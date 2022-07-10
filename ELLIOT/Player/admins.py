from ELLIOT.Cache.admins import admins
from ELLIOT.main import call_py, call_py2, call_py3, call_py4, call_py5
from pyrogram import filters
from ELLIOT.main import bot as Client
from ELLIOT.decorators import authorized_users_only
from ELLIOT.filters import command, other_filters
from ELLIOT.queues import QUEUE, clear_queue
from ELLIOT.utils import skip_current_song, skip_item
from config import BOT_USERNAME, GROUP_SUPPORT, SKIP_IMG, UPDATES_CHANNEL
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from ELLIOT.Database.clientdb import *
from ELLIOT.Database.active import remove_active_video_chat, remove_active_chat



bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 رجوع", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🗑 اغلاق", callback_data="cls")]]
)


@Client.on_message(command(["تحديث", f"adminchache"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ تم إعادة تحميل الروبوت بشكل صحيح! ** \ n✅ ** تم تحديث قائمة المشرفين ** !**"
    )


@Client.on_message(command(["تخطي", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="• القائمه", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="• اغلاق", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("❌ لا يوجد شئ في قائمة التشغيل")
        elif op == 1:
            await m.reply("✅ __قوائم الانتظار__ ** فارغة. ** \ n \ n ** • خروج المستخدم الروبوت من الدردشة الصوتية**")
        elif op == 2:
            await m.reply("🗑️ **مسح قوائم الانتظار ** \ n \ n ** • خروج المستخدم الروبوت من الدردشة الصوتية**")
        else:
            await m.reply_photo(
                photo=f"{SKIP_IMG}",
                caption=f"⌔ **تم التخطي إلى المسار التالي.**\n\n⌔ **الاسم:** [{op[0]}]({op[1]})\n⌔ **الدردشه:** `{chat_id}`\n⌔ **الحاله:** `التشغيل`\n⌔ **طلب بواسطة:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **تمت إزالة الأغنية من قائمة الانتظار:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["ايقاف", f"stop@{BOT_USERNAME}", "انهاء", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.leave_group_call(chat_id)
            if int(assistant) == 2:
               await call_py2.leave_group_call(chat_id)
            if int(assistant) == 3:
               await call_py3.leave_group_call(chat_id)
            if int(assistant) == 4:
               await call_py4.leave_group_call(chat_id)
            if int(assistant) == 5:
               await call_py5.leave_group_call(chat_id)
            await remove_active_video_chat(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await m.reply("✅ انقطع اتصال المستخدم الروبوت بالدردشة المرئية.")
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لم يتم العثور علي شئ مشغل**")


@Client.on_message(
    command(["توقف", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.pause_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.pause_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.pause_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.pause_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.pause_stream(chat_id)
            await m.reply(
                "⏸ **Track paused.**\n\n• **To resume the stream, use the**\n» /resume command."
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لاشئ في المحادثه**")


@Client.on_message(
    command(["استئناف", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.resume_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.resume_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.resume_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.resume_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.resume_stream(chat_id)
            await m.reply(
                "▶️ **استأنف المسار.**\n\n• **لإيقاف الدفق مؤقتًا ، استخدم ** \ n »/ الأمر pause."
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لاشئ في المحادثه**")


@Client.on_message(
    command(["كتم", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.mute_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.mute_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.mute_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.mute_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.mute_stream(chat_id)
            await m.reply(
                "🔇 **تم كتم الصوت.**\n\n• **لإيقاف الدفق مؤقتًا ، استخدم ** \ n »/ الأمر pause."
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لاشئ في المحادثه**")


@Client.on_message(
    command(["رفع الكتم", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.unmute_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.unmute_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.unmute_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.unmute_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.unmute_stream(chat_id)
            await m.reply(
                "🔊 **تم الغاء الكتم.**\n\n• **لكتم صوت المستخدم الروبوت استخدم**\n» /mute امر."
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لاشئ في المحادثه**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسئول مجهول! \ n \ n »قم بالعودة إلى حساب المستخدم من حقوق المسئول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⌔ المسئول وحده الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    chat_id = query.message.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.pause_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.pause_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.pause_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.pause_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.pause_stream(chat_id)
            await query.edit_message_text(
                "⏸ توقف البث مؤقتًا", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لايوجد شئ في قائمة التشغيل", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسئول مجهول! \ n \ n »قم بالعودة إلى حساب المستخدم من حقوق المسئول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⌔ المسئول وحده الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    chat_id = query.message.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.resume_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.resume_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.resume_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.resume_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.resume_stream(chat_id)
            await query.edit_message_text(
                "▶️ تم استئناف البث", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لايوجد شئ في قائمة التشغيل", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسئول مجهول! \ n \ n »قم بالعودة إلى حساب المستخدم من حقوق المسئول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⌔ المسئول وحده الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    chat_id = query.message.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.leave_group_call(chat_id)
            if int(assistant) == 2:
               await call_py2.leave_group_call(chat_id)
            if int(assistant) == 3:
               await call_py3.leave_group_call(chat_id)
            if int(assistant) == 4:
               await call_py4.leave_group_call(chat_id)
            if int(assistant) == 5:
               await call_py5.leave_group_call(chat_id)
            await remove_active_video_chat(chat_id)
            await remove_active_chat(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("✅ **انتهي هذا المشغل**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لايوجد شئ في قائمة التشغيل", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسئول مجهول! \ n \ n »قم بالعودة إلى حساب المستخدم من حقوق المسئول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⌔ المسئول وحده الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    chat_id = query.message.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.mute_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.mute_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.mute_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.mute_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.mute_stream(chat_id)
            await query.edit_message_text(
                "🔇 تم كتم صوت المساعد بنجاح", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لايوجد شئ في قائمة التشغيل", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("أنت مسئول مجهول! \ n \ n »قم بالعودة إلى حساب المستخدم من حقوق المسئول.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("⌔ المسئول وحده الذي لديه إذن إدارة الدردشات الصوتية يمكنه النقر على هذا الزر!", show_alert=True)
    chat_id = query.message.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.unmute_stream(chat_id)
            if int(assistant) == 2:
               await call_py2.unmute_stream(chat_id)
            if int(assistant) == 3:
               await call_py3.unmute_stream(chat_id)
            if int(assistant) == 4:
               await call_py4.unmute_stream(chat_id)
            if int(assistant) == 5:
               await call_py5.unmute_stream(chat_id)
            await query.edit_message_text(
                "🔊 تم الغاء كتم المساعد بنجاح", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"🚫 **خطأ:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("❌ لايوجد شئ في قائمة التشغيل", show_alert=True)


@Client.on_message(
    command(["صوت", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    if chat_id in QUEUE:
        try:
            if int(assistant) == 1:
               await call_py.change_volume_call(chat_id, volume=int(range))
            if int(assistant) == 2:
               await call_py2.change_volume_call(chat_id, volume=int(range))
            if int(assistant) == 3:
               await call_py3.change_volume_call(chat_id, volume=int(range))
            if int(assistant) == 4:
               await call_py4.change_volume_call(chat_id, volume=int(range))
            if int(assistant) == 5:
               await call_py5.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"✅ **ضبط الصوت** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"🚫 **خطأ:**\n\n`{e}`")
    else:
        await m.reply("❌ **لاشئ في المحادثه**")