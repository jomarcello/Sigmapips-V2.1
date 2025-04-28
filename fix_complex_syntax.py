with open('trading_bot/services/telegram_service/bot.py', 'r') as f:
    lines = f.readlines()

# Find the start of the method containing the problematic code
# Look for a line containing "def menu_signals_callback"
method_start = 0
for i, line in enumerate(lines):
    if "def menu_signals_callback" in line:
        method_start = i
        break

if method_start == 0:
    print("Could not find menu_signals_callback method")
    exit(1)

# Create a corrected version of the entire method - using triple-quotes correctly
fixed_method = '''    async def menu_signals_callback(self, update: Update, context=None) -> int:
        """Handle menu_signals button press"""
        query = update.callback_query
        await query.answer()
        
        # Clear any previous context variables to avoid confusion
        if context and hasattr(context, 'user_data'):
            # Keep only essential data
            preserved_data = {}
            for key in ['user_id', 'username', 'first_name', 'subscription']:
                if key in context.user_data:
                    preserved_data[key] = context.user_data[key]
            
            # Reset user_data and restore only what we need
            context.user_data.clear()
            for key, value in preserved_data.items():
                context.user_data[key] = value
            
            # Set flags for proper menu navigation
            context.user_data['from_signal'] = False
            context.user_data['is_signals_context'] = True
            
            logger.info(f"Updated context in menu_signals_callback: {context.user_data}")
        
        # Create keyboard for signal menu
        keyboard = [
            [InlineKeyboardButton("➕ Add Signal", callback_data="signals_add")],
            [InlineKeyboardButton("📊 Manage Signals", callback_data="signals_manage")],
            [InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Get the signals GIF URL for better UX
        signals_gif_url = "https://media.giphy.com/media/gSzIKNrqtotEYrZv7i/giphy.gif"
        signals_caption = "<b>📈 Signal Management</b>\\n\\nManage your trading signals"
        
        # Try to update the message with the GIF and caption
        try:
            # First, try deleting the old message and sending a new one with the GIF
            try:
                await query.message.delete()
                await context.bot.send_animation(
                    chat_id=update.effective_chat.id,
                    animation=signals_gif_url,
                    caption=signals_caption,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            except Exception as delete_error:
                logger.warning(f"Could not delete message, trying media update: {delete_error}")
                # If deletion fails, try editing the media
                try:
                    await query.edit_message_media(
                        media=InputMediaAnimation(
                            media=signals_gif_url,
                            caption=signals_caption,
                            parse_mode=ParseMode.HTML
                        ),
                        reply_markup=reply_markup
                    )
                except Exception as media_error:
                    logger.warning(f"Could not update media, trying text update: {media_error}")
                    # If media edit fails, try editing text/caption
                    try:
                        await query.edit_message_text(
                            text=signals_caption,
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML
                        )
                    except Exception as text_error:
                        if "There is no text in the message to edit" in str(text_error):
                            try:
                                await query.edit_message_caption(
                                    caption=signals_caption,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
                            except Exception as caption_error:
                                logger.error(f"Failed to update caption: {caption_error}")
                                # Last resort: Send a new message
                                await context.bot.send_animation(
                                    chat_id=update.effective_chat.id,
                                    animation=signals_gif_url,
                                    caption=signals_caption,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML
                                )
                        else:
                            logger.error(f"Failed to update text message: {text_error}")
                            # Last resort: Send a new message
                            await context.bot.send_animation(
                                chat_id=update.effective_chat.id,
                                animation=signals_gif_url,
                                caption=signals_caption,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML
                            )
        except Exception as e:
            logger.error(f"Error updating message: {e}")
            # Absolute last resort
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=signals_caption,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.HTML
                )
            except Exception as final_error:
                logger.error(f"All message update attempts failed: {final_error}")
        
        return SIGNALS  # Return the signals menu state'''

# Find the end of the method by looking for the next def statement
method_end = 0
for i in range(method_start + 1, len(lines)):
    if "    async def" in lines[i] or "    def" in lines[i]:
        method_end = i
        break

if method_end == 0:
    # If we can't find the next method, just go to the end of the file
    method_end = len(lines)

# Replace the entire method with our fixed version
fixed_method_lines = fixed_method.split('\n')
fixed_method_lines = [line + '\n' for line in fixed_method_lines]

# Construct new file contents
new_lines = lines[:method_start] + fixed_method_lines + lines[method_end:]

# Also fix the else: at line 1240
for i, line in enumerate(new_lines):
    if i+1 == 1240 and 'else:' in line and not line.strip().startswith('else:'):
        # This appears to be a misplaced else
        # Get indentation level that would be correct
        correct_indent = ' ' * 12  # Based on surrounding code
        new_lines[i] = correct_indent + 'else:\n'

with open('trading_bot/services/telegram_service/bot.py', 'w') as f:
    f.writelines(new_lines)

print("Fixed complex syntax issues") 