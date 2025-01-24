def get_room_name_for_users(user_a_id, user_b_id):
    """
    Generate a unique room name for a chat between two users.

    This function ensures that the room name is consistent regardless of the order
    of the user IDs by always placing the smaller ID first.

    Args:
        user_a_id (int): The ID of the first user.
        user_b_id (int): The ID of the second user.

    Returns:
        str: A string representing the unique room name for the chat.
    """
    if user_a_id > user_b_id:
        user_a_id, user_b_id = user_b_id, user_a_id
    return f"chat_{user_a_id}_{user_b_id}"
