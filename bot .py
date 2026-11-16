import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# الـ ID الخاص بك (المستخدم الوحيد المصرح له)
ALLOWED_USER_ID = 8693481980
# يوزر قناتك العامة
CHANNEL_USERNAME = "@privet_groub"

# تحميل الأرقام من الملفات
def load_numbers(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

egypt_whatsapp_numbers = load_numbers("numbers_Egypt_WE_RS01_173.txt")
laos_whatsapp_numbers = load_numbers("Laos.txt")
guatemala_whatsapp_numbers = load_numbers("Guatemala.txt")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def is_owner(update: Update) -> bool:
    user = update.effective_user
    return user and user.id == ALLOWED_USER_ID

# 1. أمر /start والشاشة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.message.reply_text("عذراً، هذا البوت خاص ولا يمكن للآخرين استخدامه 🔒")
        return

    keyboard = [
        [InlineKeyboardButton("🟢 Get number", callback_data="get_number")],
        [
            InlineKeyboardButton("📊 Live Traffic", callback_data="live_traffic"),
            InlineKeyboardButton("📈 My Stats", callback_data="my_stats"),
        ],
        [InlineKeyboardButton("💰 My Wallet", callback_data="my_wallet")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "🌐 ~ { **WELCOME** } ~ 🌐\n\n"
        "📊 **Your World of Virtual Numbers**\n"
        "⚡ **Fast & Reliable Service**\n\n"
        "📥 **Select an option below to get started:**"
    )
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.from_user.id != ALLOWED_USER_ID:
        await query.answer("هذا البوت ليس مخصصاً لك!", show_alert=True)
        return

    await query.answer()
    data = query.data

    if data == "get_number":
        # عرض المنصات
        keyboard = [
            [InlineKeyboardButton("✈️ Telegram", callback_data="serv_telegram")],
            [InlineKeyboardButton("💬 WhatsApp", callback_data="serv_whatsapp")],
            [InlineKeyboardButton("📘 Facebook", callback_data="serv_facebook")],
        ]
        await query.edit_message_text(
            text="⚙️ **Select a Service:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "serv_whatsapp":
        # عرض دول الواتساب المتاحة (مصر + لاوس + غواتيمالا)
        egypt_count = len(egypt_whatsapp_numbers)
        laos_count = len(laos_whatsapp_numbers)
        guatemala_count = len(guatemala_whatsapp_numbers)
        
        keyboard = [
            [InlineKeyboardButton(f"🇪🇬 Egypt (WE) - ({egypt_count}) - 0.0001 USD", callback_data="get_egypt_num")],
            [InlineKeyboardButton(f"🇱🇦 Laos - ({laos_count}) - 0.0001 USD", callback_data="get_laos_num")],
            [InlineKeyboardButton(f"🇬🇹 Guatemala - ({guatemala_count}) - 0.0001 USD", callback_data="get_guatemala_num")],
            [InlineKeyboardButton("« Go Back", callback_data="get_number")]
        ]
        await query.edit_message_text(
            text="🌍 **Select a Country for WhatsApp:**",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data == "serv_telegram":
        await query.edit_message_text(
            text="⚠️ لا توجد أرقام تليجرام متاحة حالياً.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Go Back", callback_data="get_number")]])
        )

    elif data == "get_egypt_num":
        if not egypt_whatsapp_numbers:
            await query.edit_message_text(text="❌ عذراً، نفدت أرقام مصر (واتساب) من الملف حالياً!")
            return

        selected_number = egypt_whatsapp_numbers.pop(0)
        masked_num = selected_number[:4] + "****" + selected_number[-4:]
        
        private_text = (
            f"📱 **ASSIGNED FOR YOU** ✅\n\n"
            f"💬 Service: WhatsApp (Egypt)\n"
            f"📞 Number: `+{selected_number}`\n\n"
            f"⏳ في انتظار وصول الكود..."
        )
        
        keyboard = [
            [InlineKeyboardButton(f"+{selected_number}", callback_data="copy_num")],
            [InlineKeyboardButton("🔄 Change Number", callback_data="get_egypt_num")],
            [InlineKeyboardButton("🔙 Change Country", callback_data="serv_whatsapp")],
            [InlineKeyboardButton("📢 OTP Group", url=f"https://t.me/privet_groub")]
        ]
        
        await query.edit_message_text(text=private_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
        try:
            channel_msg = f"🔐 **New Number Assigned**\n💬 Service: WhatsApp (Egypt)\n📞 Number: `+{masked_num}`"
            await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=channel_msg, parse_mode="Markdown")
        except Exception as e:
            print(f"خطأ في النشر بالقناة: {e}")

    elif data == "get_laos_num":
        if not laos_whatsapp_numbers:
            await query.edit_message_text(text="❌ عذراً، نفدت أرقام لاوس (واتساب) من الملف حالياً!")
            return

        selected_number = laos_whatsapp_numbers.pop(0)
        masked_num = selected_number[:4] + "****" + selected_number[-4:]
        
        private_text = (
            f"📱 **ASSIGNED FOR YOU** ✅\n\n"
            f"💬 Service: WhatsApp (Laos)\n"
            f"📞 Number: `+{selected_number}`\n\n"
            f"⏳ في انتظار وصول الكود..."
        )
        
        keyboard = [
            [InlineKeyboardButton(f"+{selected_number}", callback_data="copy_num")],
            [InlineKeyboardButton("🔄 Change Number", callback_data="get_laos_num")],
            [InlineKeyboardButton("🔙 Change Country", callback_data="serv_whatsapp")],
            [InlineKeyboardButton("📢 OTP Group", url=f"https://t.me/privet_groub")]
        ]
        
        await query.edit_message_text(text=private_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
        try:
            channel_msg = f"🔐 **New Number Assigned**\n💬 Service: WhatsApp (Laos)\n📞 Number: `+{masked_num}`"
            await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=channel_msg, parse_mode="Markdown")
        except Exception as e:
            print(f"خطأ في النشر بالقناة: {e}")

    elif data == "get_guatemala_num":
        if not guatemala_whatsapp_numbers:
            await query.edit_message_text(text="❌ عذراً، نفدت أرقام غواتيمالا (واتساب) من الملف حالياً!")
            return

        selected_number = guatemala_whatsapp_numbers.pop(0)
        masked_num = selected_number[:4] + "****" + selected_number[-4:]
        
        private_text = (
            f"📱 **ASSIGNED FOR YOU** ✅\n\n"
            f"💬 Service: WhatsApp (Guatemala)\n"
            f"📞 Number: `+{selected_number}`\n\n"
            f"⏳ في انتظار وصول الكود..."
        )
        
        keyboard = [
            [InlineKeyboardButton(f"+{selected_number}", callback_data="copy_num")],
            [InlineKeyboardButton("🔄 Change Number", callback_data="get_guatemala_num")],
            [InlineKeyboardButton("🔙 Change Country", callback_data="serv_whatsapp")],
            [InlineKeyboardButton("📢 OTP Group", url=f"https://t.me/privet_groub")]
        ]
        
        await query.edit_message_text(text=private_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        
        try:
            channel_msg = f"🔐 **New Number Assigned**\n💬 Service: WhatsApp (Guatemala)\n📞 Number: `+{masked_num}`"
            await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=channel_msg, parse_mode="Markdown")
        except Exception as e:
            print(f"خطأ في النشر بالقناة: {e}")

    elif data == "serv_facebook":
        await query.edit_message_text(
            text="⚠️ هذه الخدمة غير متوفرة حالياً.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("« Go Back", callback_data="get_number")]])
        )
    
    elif data == "live_traffic":
        await query.edit_message_text(text="📊 Live Traffic: الأنشطة تعمل بشكل سليم.")
    elif data == "my_stats":
        stats_text = (
            f"📈 إحصائياتك:\n"
            f"- أرقام مصر (واتساب): {len(egypt_whatsapp_numbers)}\n"
            f"- أرقام لاوس (واتساب): {len(laos_whatsapp_numbers)}\n"
            f"- أرقام غواتيمالا (واتساب): {len(guatemala_whatsapp_numbers)}"
        )
        await query.edit_message_text(text=stats_text)
    elif data == "my_wallet":
        await query.edit_message_text(text="💰 محفظتك الحالية: $0.00")

if __name__ == "__main__":
    TOKEN = "8729199445:AAGVwW0Jju7hjZrFTJin8yRf_Lq1mPzsKro"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("تم إضافة غواتيمالا بنجاح وتحديث البوت بالكامل 🚀")
    app.run_polling()