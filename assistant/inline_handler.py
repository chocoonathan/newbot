from command import (alive_inline, button_inline, get_inline_help,
                     get_inline_note, google_search_func, inline_afk,
                     inline_anime, inline_apkan1, inline_apkmoddy,
                     inline_autobc, inline_bmkg, inline_bola,
                     inline_calculator, inline_cancel, inline_card_info,
                     inline_cat, inline_chatai, inline_chord, inline_comic,
                     inline_donghua, inline_font, inline_help_func,
                     inline_info, inline_news, inline_otaku_search,
                     inline_spotify, inline_streaming, inline_youtube,
                     inline_youtube_search, lk21_search_func_v2,
                     pmpermit_inline, send_inline)
from helpers import CMD


@CMD.INLINE()
async def _(client, inline_query):
    try:
        text = inline_query.query.strip().lower()
        answers = []
        if text.strip() == "":
            answerss = await inline_help_func(_)
            return await client.answer_inline_query(
                inline_query.id, results=answerss, cache_time=10
            )
        elif text.split()[0] == "help":
            answerss = await get_inline_help(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id, results=answerss, cache_time=0
            )
        elif text.split()[0] == "alive":
            answerss = await alive_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_send":
            tuju = text.split()[1]
            answerss = await send_inline(answers, inline_query, int(tuju))
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "make_button":
            tuju = text.split()[1]
            answerss = await button_inline(answers, inline_query, int(tuju))
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "pmpermit_inline":
            answerss = await pmpermit_inline(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "get_note":
            answerss = await get_inline_note(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_font":
            answerss = await inline_font(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_cat":
            answerss = await inline_cat(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_bola":
            answerss = await inline_bola(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_spotify":
            answerss = await inline_spotify(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_news":
            answerss = await inline_news(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_anime":
            answerss = await inline_anime(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_donghua":
            answerss = await inline_donghua(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_comic":
            answerss = await inline_comic(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )

        elif text.split()[0] == "inline_chatai":
            answerss = await inline_chatai(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_info":
            answerss = await inline_info(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_card_info":
            answerss = await inline_card_info(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_chord":
            answerss = await inline_chord(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_apkan1":
            answerss = await inline_apkan1(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_afk":
            answerss = await inline_afk(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_bmkg":
            answerss = await inline_bmkg(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_youtube":
            answerss = await inline_youtube(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_apkmoddy":
            answerss = await inline_apkmoddy(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_autobc":
            answerss = await inline_autobc(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_cancel":
            answerss = await inline_cancel(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "inline_streaming":
            answerss = await inline_streaming(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] in ["calculator", "calc", "kalkulator"]:
            answerss = await inline_calculator(answers, inline_query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answerss,
                cache_time=0,
            )
        elif text.split()[0] == "google":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    inline_query.id,
                    results=answers,
                    switch_pm_text="🔍 Google Search - ketik: google [query]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answers = await google_search_func(answers, tex)
            return await client.answer_inline_query(
                inline_query.id,
                results=answers,
            )
        elif text.split()[0] == "lk21":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    inline_query.id,
                    results=answers,
                    switch_pm_text="🔍 LK21 Search - ketik: lk21 [query]",
                    switch_pm_parameter="inline",
                )
            tex = text.split(None, 1)[1].strip()
            answers = await lk21_search_func_v2(answers, tex)
            return await client.answer_inline_query(
                inline_query.id,
                results=answers,
            )
        elif text.split()[0] == "otaku":
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    inline_query.id,
                    results=answers,
                    switch_pm_text="🔍 Otaku Search - ketik: otaku [query]",
                    switch_pm_parameter="inline",
                )

            query = text.split(None, 1)[1].strip()
            answers = await inline_otaku_search(answers, query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answers,
            )
        elif text.split()[0] in ["youtube", "yt"]:
            if len(text.split()) < 2:
                return await client.answer_inline_query(
                    inline_query.id,
                    results=answers,
                    switch_pm_text="🎬 YouTube Search - ketik: youtube [query]",
                    switch_pm_parameter="inline",
                )

            query = text.split(None, 1)[1].strip()
            answers = await inline_youtube_search(answers, query)
            return await client.answer_inline_query(
                inline_query.id,
                results=answers,
                cache_time=300,
            )
    except Exception:
        raise
