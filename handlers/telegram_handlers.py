from telegram import Update
from telegram.ext import CallbackContext
from post.models import Post

def get_user_info_handler(update: Update, context: CallbackContext):
    # Получение информации о пользователе из базы данных
    post = Post.objects.get(title='title')

    # Отправка информации пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"title: {post.title}, author: {post.author}")
