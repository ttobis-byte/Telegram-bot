import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


ARKANAI = {
    1: ("INFORMACIJA", "Neįklimpti į tuščius pokalbius, apkalbas, perteklinę informaciją ir pažadus be veiksmų. Žodžius paverskite veiksmais."),
    2: ("SVEIKATA", "Neužsiciklinkite ties sveikata, mityba, dietomis, sportu ar išvaizda. Rūpinkitės savimi be kraštutinumų."),
    3: ("VAIKAI IR KŪRYBA", "Nepaverskite vaikų vieninteliu gyvenimo tikslu. Venkite perdėtos globos ir prisirišimo prie savo idėjų."),
    4: ("KARJERA", "Neįklimkite į darbą ir darboholizmą. Karjera neturi pakeisti viso gyvenimo."),
    5: ("DVASINĖS PRAKTIKOS", "Neužsidarykite vien dvasinėse praktikose ir teorijose. Žinias pritaikykite realiame gyvenime."),
    6: ("ŠEIMA IR MEILĖ", "Rūpinkitės kitais, bet neaukokite savęs. Palikite artimiesiems atsakomybę už jų pačių gyvenimą."),
    7: ("RIBOS IR KELIONĖS", "Saugokite savo ribas, bet nepaverskite laisvės nuolatiniu bėgimu nuo įsipareigojimų."),
    8: ("TEISINGUMAS", "Neįklimkite į ginčus, teisumo įrodinėjimą ir svetimų problemų sprendimą."),
    9: ("SAVIPAKANKAMUMAS", "Savipakankamumo nepaverskite izoliacija. Leiskite sau priimti kitų žmonių pagalbą."),
    10: ("KARJEROS SIEKIS", "Neleiskite nuolatiniam rezultatų ir statuso siekimui tapti vieninteliu gyvenimo tikslu."),
    11: ("DRAUGAI IR KONFLIKTAI", "Neįsitraukite į svetimus konfliktus ir gelbėtojo vaidmenį. Atskirkit savo atsakomybę nuo kitų."),
    12: ("ASKETIZMAS", "Neužstrikite aukojimosi ir savęs ribojimo būsenoje. Leiskite sau ne tik duoti, bet ir gauti."),
    13: ("KRIZĖS", "Neieškokite nuolatinių krizių ir griovimo. Pokyčius naudokite atsinaujinimui."),
    14: ("NUOBODULYS", "Neįklimkite į monotoniją ir laukimą. Kurkite judėjimą ir naują patirtį."),
    15: ("PRIKLAUSOMYBĖS", "Stebėkite prisirišimus, pagundas ir priklausomybes. Neleiskite jiems valdyti jūsų pasirinkimų."),
    16: ("GRIŪTIS", "Negriaukite to, ką galima pertvarkyti. Krizę naudokite naujam pagrindui sukurti."),
    17: ("ILIUZIJOS", "Neužstrikite svajonėse ir idealizavime. Tikrinkite savo lūkesčius realiais veiksmais."),
    18: ("UŽSIDARYMAS NAMUOSE", "Neužsidarykite savo saugioje erdvėje. Palaikykite ryšį su išoriniu pasauliu."),
    19: ("ĮVAIZDIS IR ŠLOVĖ", "Neleiskite įvaizdžiui ir kitų pripažinimui tapti jūsų vertės matu."),
    20: ("VISUOMENĖ IR TEISĖ", "Neprisiimkite visos visuomenės problemų. Atskirkit savo atsakomybę nuo kolektyvinės."),
    21: ("TRIUMFAS", "Neužstrikite ties pasiekimais ir noru visada laimėti. Po rezultato leiskite sau judėti toliau."),
    22: ("LAISVĖ IR KELIONĖS", "Laisvės nepaverskite bėgimu nuo atsakomybės. Derinkite spontaniškumą su stabilumu.")
}


def likimo_spastai(diena, menuo, metai):
    dt = diena
    if dt > 22:
        dt -= 22

    mt = menuo

    gt = sum(int(x) for x in str(metai))
    while gt > 22:
        gt = sum(int(x) for x in str(gt))

    suma = dt + mt + gt
    if suma > 22:
        suma -= 22

    rezultatas = abs(abs(dt - mt) - suma)

    while rezultatas > 22:
        rezultatas -= 22

    return rezultatas


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sveiki! 👋\n\n"
        "LIKIMO SPĄSTAI\n\n"
        "Įveskite savo gimimo datą formatu:\n"
        "28.08.1974"
    )


async def skaiciuoti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tekstas = update.message.text.strip()

    try:
        data = datetime.strptime(tekstas, "%d.%m.%Y")
    except ValueError:
        await update.message.reply_text(
            "Įveskite gimimo datą formatu:\n"
            "28.08.1974"
        )
        return

    rezultatas = likimo_spastai(
        data.day,
        data.month,
        data.year
    )

    if rezultatas not in ARKANAI:
        await update.message.reply_text(
            f"Rezultatas: {rezultatas}"
        )
        return

    pavadinimas, rekomendacija = ARKANAI[rezultatas]

    await update.message.reply_text(
        f"Rezultatas: {rezultatas}\n\n"
        f"{rezultatas} ARKANAS\n\n"
        f"{pavadinimas}\n\n"
        f"Rekomendacija:\n{rekomendacija}"
    )


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN nerastas")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, skaiciuoti))

    print("Botas paleistas.")
    app.run_polling()


if __name__ == "__main__":
    main()
