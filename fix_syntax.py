with open('trading_bot/services/telegram_service/bot.py', 'r') as f:
    lines = f.readlines()

# Get the raw text from lines 2980-3060
raw_block = """        signals_caption = "<b>📈 Signal Management</b>\\n\\nManage your trading signals"
        
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
        
        return SIGNALS # Return the signals menu state"""

# Split into lines
fixed_block_lines = raw_block.split('\n')

# Replace the problematic section in the original file
start_line = 2980
end_line = start_line + len(fixed_block_lines)
new_lines = lines[:start_line-1] + [line + '\n' for line in fixed_block_lines] + lines[end_line-1:]

# Now fix the 'else:' issue at line 1240
for i, line in enumerate(new_lines):
    if i+1 == 1240 and 'else:' in line and not line.strip().startswith('else:'):
        # This appears to be a misplaced else
        # Get indentation level that would be correct
        correct_indent = ' ' * 12  # Based on surrounding code
        new_lines[i] = correct_indent + 'else:\n'

with open('trading_bot/services/telegram_service/bot.py', 'w') as f:
    f.writelines(new_lines)

print("Fixed syntax issues") 