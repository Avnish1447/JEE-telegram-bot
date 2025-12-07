"""
Poll Handler for Mentor Tracking Bot
Handles poll creation and vote tracking
"""

from telegram import Update, Poll
from telegram.ext import ContextTypes
import database as db
import config


async def create_poll_in_group(context: ContextTypes.DEFAULT_TYPE, group_id: int):
    """
    Creates a poll in a specific group with mentors as options.
    
    This function is called by the scheduler to send polls automatically.
    
    Args:
        context: Bot context
        group_id: ID of the group where poll should be sent
    
    Returns:
        bool: True if poll was created successfully
    """
    
    try:
        # Get all mentors in this group
        mentors = db.get_mentors_by_group(group_id)
        
        if not mentors or len(mentors) < 2:
            print(f"⚠️  Not enough mentors in group {group_id} to create poll (need at least 2)")
            return False
        
        # Create poll options (mentor names)
        options = [mentor['full_name'] for mentor in mentors]
        
        # Send the poll
        poll_message = await context.bot.send_poll(
            chat_id=group_id,
            question=config.POLL_QUESTION,
            options=options,
            is_anonymous=True,  # Anonymous voting
            allows_multiple_answers=False  # Single choice only
        )
        
        # Get the poll ID
        poll_id = poll_message.poll.id
        
        # Save poll to database
        db.create_poll(poll_id, group_id)
        
        print(f"✅ Poll created in group {group_id} with {len(options)} mentors")
        return True
        
    except Exception as e:
        print(f"❌ Error creating poll in group {group_id}: {e}")
        return False


async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles when a user votes in a poll.
    
    This function is triggered whenever someone votes in any poll.
    It logs the vote to the database.
    
    Args:
        update: Telegram update object containing poll answer
        context: Bot context
    """
    
    # Get poll answer data
    poll_answer = update.poll_answer
    
    if not poll_answer:
        return
    
    poll_id = poll_answer.poll_id
    voter_id = poll_answer.user.id
    option_ids = poll_answer.option_ids
    
    # Check if user actually selected an option
    if not option_ids:
        return
    
    # Get the selected option index (first one, since we only allow single choice)
    selected_option_index = option_ids[0]
    
    try:
        # We need to map the option index to a mentor
        # This requires us to know which poll this is and what the options were
        # For now, we'll store the option index and resolve it later
        # In a production system, you'd want to cache poll data
        
        # Get poll from database to find the group
        # Note: We'll need to enhance the database to store poll options
        # For now, we'll use a simplified approach
        
        print(f"📊 Vote received: Poll {poll_id}, Voter {voter_id}, Option {selected_option_index}")
        
        # TODO: Map option index to mentor_id and log vote
        # This will be implemented when we have poll option mapping
        
    except Exception as e:
        print(f"❌ Error handling poll answer: {e}")


async def handle_poll_answer_enhanced(update: Update, context: ContextTypes.DEFAULT_TYPE, poll_data: dict):
    """
    Enhanced poll answer handler with poll data mapping.
    
    This version requires poll data to be stored in bot context.
    
    Args:
        update: Telegram update object
        context: Bot context
        poll_data: Dictionary mapping poll_id to mentor list
    """
    
    poll_answer = update.poll_answer
    
    if not poll_answer:
        return
    
    poll_id = poll_answer.poll_id
    voter_id = poll_answer.user.id
    option_ids = poll_answer.option_ids
    
    if not option_ids:
        return
    
    selected_option_index = option_ids[0]
    
    try:
        # Get poll data from context
        if poll_id not in poll_data:
            print(f"⚠️  Poll {poll_id} not found in poll data")
            return
        
        poll_info = poll_data[poll_id]
        mentors = poll_info['mentors']
        group_id = poll_info['group_id']
        
        # Get the mentor who was voted for
        if selected_option_index >= len(mentors):
            print(f"❌ Invalid option index {selected_option_index}")
            return
        
        selected_mentor = mentors[selected_option_index]
        mentor_id = selected_mentor['mentor_id']
        
        # Log the vote
        success = db.log_vote(poll_id, mentor_id, voter_id, group_id)
        
        if success:
            print(f"✅ Vote logged: {selected_mentor['full_name']} got a vote in poll {poll_id}")
        else:
            print(f"❌ Failed to log vote")
            
    except Exception as e:
        print(f"❌ Error handling poll answer: {e}")


async def send_test_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Admin command to send a test poll immediately.
    
    Usage: /send_poll
    
    Sends a poll in the current group for testing purposes.
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    
    user_id = update.effective_user.id
    
    # Check if user is admin
    if not config.is_admin(user_id):
        await update.message.reply_text("❌ You don't have permission to use this command.")
        return
    
    group_id = update.effective_chat.id
    
    # Check if this is a group
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("❌ This command can only be used in groups.")
        return
    
    # Create poll with tracking
    success = await create_poll_with_tracking(context, group_id)
    
    if success:
        await update.message.reply_text("✅ Test poll sent!")
    else:
        await update.message.reply_text("❌ Failed to send poll. Make sure there are at least 2 mentors in this group.")


# ==================== POLL DATA STORAGE ====================

# Global dictionary to store poll data
# In production, you might want to use Redis or a database for this
POLL_DATA = {}


def store_poll_data(poll_id: str, mentors: list, group_id: int):
    """
    Stores poll data for later retrieval when processing votes.
    
    Args:
        poll_id: ID of the poll
        mentors: List of mentor dictionaries
        group_id: Group where poll was sent
    """
    POLL_DATA[poll_id] = {
        'mentors': mentors,
        'group_id': group_id
    }


async def create_poll_with_tracking(context: ContextTypes.DEFAULT_TYPE, group_id: int):
    """
    Creates a poll and stores the poll data for vote tracking.
    
    This is the recommended function to use for creating polls.
    
    Args:
        context: Bot context
        group_id: ID of the group where poll should be sent
    
    Returns:
        bool: True if successful
    """
    
    try:
        # Get all mentors in this group
        mentors = db.get_mentors_by_group(group_id)
        
        if not mentors or len(mentors) < 2:
            print(f"⚠️  Not enough mentors in group {group_id}")
            return False
        
        # Create poll options
        options = [mentor['full_name'] for mentor in mentors]
        
        # Send the poll
        poll_message = await context.bot.send_poll(
            chat_id=group_id,
            question=config.POLL_QUESTION,
            options=options,
            is_anonymous=True,
            allows_multiple_answers=False
        )
        
        poll_id = poll_message.poll.id
        
        # Store poll data for vote tracking
        store_poll_data(poll_id, mentors, group_id)
        
        # Save poll to database
        db.create_poll(poll_id, group_id)
        
        print(f"✅ Poll created and tracked in group {group_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating poll: {e}")
        return False


async def handle_poll_answer_with_tracking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles poll answers using stored poll data.
    
    This is the main poll answer handler to use.
    
    Args:
        update: Telegram update object
        context: Bot context
    """
    
    poll_answer = update.poll_answer
    
    if not poll_answer:
        return
    
    poll_id = poll_answer.poll_id
    voter_id = poll_answer.user.id
    option_ids = poll_answer.option_ids
    
    if not option_ids:
        return
    
    selected_option_index = option_ids[0]
    
    try:
        # Get poll data
        if poll_id not in POLL_DATA:
            print(f"⚠️  Poll {poll_id} not found in tracking data")
            return
        
        poll_info = POLL_DATA[poll_id]
        mentors = poll_info['mentors']
        group_id = poll_info['group_id']
        
        # Get selected mentor
        if selected_option_index >= len(mentors):
            print(f"❌ Invalid option index")
            return
        
        selected_mentor = mentors[selected_option_index]
        mentor_id = selected_mentor['mentor_id']
        
        # Log the vote
        success = db.log_vote(poll_id, mentor_id, voter_id, group_id)
        
        if success:
            print(f"✅ Vote logged: {selected_mentor['full_name']} received a vote")
        
    except Exception as e:
        print(f"❌ Error handling poll answer: {e}")


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    print("""
    Poll Handler Module
    ===================
    
    This module handles poll creation and vote tracking.
    
    Key Functions:
    
    1. create_poll_with_tracking(context, group_id)
       - Creates a poll in a group
       - Stores poll data for vote tracking
       - Called by scheduler
    
    2. handle_poll_answer_with_tracking(update, context)
       - Handles when users vote
       - Maps votes to mentors
       - Logs votes to database
    
    3. send_test_poll(update, context)
       - Admin command to test polls
       - Usage: /send_poll
    
    How it works:
    1. Scheduler calls create_poll_with_tracking()
    2. Poll is sent with mentor names as options
    3. User votes in the poll
    4. handle_poll_answer_with_tracking() captures the vote
    5. Vote is logged to database
    """)
