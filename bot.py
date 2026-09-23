import os
import re
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


ARKANAI = {
    1: (
        "INFORMACIJA",
        [
            "Įstrigimas nuolatiniame informacijos rinkime.",
            "Tušti pokalbiai ir apkalbos.",
            "Perteklinis kalbėjimas vietoj veiksmų.",
            "Pažadai, kurie nevirsta konkrečiais darbais.",
        ],
        "Neužstrikite informacijoje ir tuščiuose pokalbiuose. "
        "Mažiau kalbėkite apie tai, ką darysite, ir daugiau veikite. "
        "Žodžius paverskite konkrečiais veiksmais.",
    ),
    2: (
        "SVEIKATA",
        [
            "Perdėtas susitelkimas į sveikatą.",
            "Nuolatinis dietų ir mitybos sistemų ieškojimas.",
            "Perdėtas dėmesys sportui ar išvaizdai.",
            "Užsiciklinimas ties kūno būkle arba mama.",
        ],
        "Rūpinkitės savo kūnu ir sveikata, tačiau nepaverskite to pagrindiniu "
        "gyvenimo centru. Ieškokite pusiausvyros, o ne kraštutinumų.",
    ),
    3: (
        "VAIKAI IR KŪRYBA",
        [
            "Vaikų pavertimas vieninteliu gyvenimo tikslu.",
            "Perdėta vaikų globa ir kontrolė.",
            "Prisirišimas prie savo kūrybinių idėjų.",
            "Sunkumas leisti vaikams ar savo kūriniams gyventi savarankiškai.",
        ],
        "Mylėkite ir rūpinkitės, bet neperimkite kito žmogaus gyvenimo. "
        "Leiskite vaikams ir savo kūrybai vystytis savarankiškai.",
    ),
    4: (
        "KARJERA",
        [
            "Darboholizmas.",
            "Gyvenimas vien darbu ir pareigomis.",
            "Savivertės siejimas tik su profesiniais rezultatais.",
            "Asmeninio gyvenimo nustūmimas į antrą planą.",
        ],
        "Neįklimpkite į darbą ir darboholizmą. Karjera yra gyvenimo dalis, "
        "bet ji neturi pakeisti viso gyvenimo.",
    ),
    5: (
        "DVASINĖS PRAKTIKOS",
        [
            "Nuolatinis naujų mokymų ir teorijų ieškojimas.",
            "Gyvenimas vien dvasinėmis praktikomis.",
            "Žinių kaupimas jų nepritaikant.",
            "Bėgimas nuo realaus gyvenimo į teorijas.",
        ],
        "Neužsidarykite vien dvasinėse praktikose ir teorijose. "
        "Įgytas žinias pritaikykite realiame gyvenime.",
    ),
    6: (
        "ŠEIMA IR MEILĖ",
        [
            "Idealios šeimos paieška.",
            "Perdėtas rūpinimasis kitais.",
            "Šeimos interesų iškėlimas aukščiau savųjų.",
            "Nuolatinis artimųjų gelbėjimas.",
            "Idealaus partnerio laukimas.",
        ],
        "Rūpinkitės kitais, bet neaukokite savęs. "
        "Palikite artimiesiems atsakomybę už jų pačių gyvenimą.",
    ),
    7: (
        "RIBOS IR KELIONĖS",
        [
            "Nuolatinis noras pabėgti nuo įsipareigojimų.",
            "Laisvės pavertimas gyvenimo tikslu.",
            "Sunkumas priimti ribas.",
            "Nuolatinis judėjimas neįsitvirtinant.",
        ],
        "Saugokite savo ribas, bet nepaverskite laisvės nuolatiniu bėgimu "
        "nuo įsipareigojimų.",
    ),
    8: (
        "TEISINGUMAS",
        [
            "Įsitraukimas į ginčus.",
            "Nuolatinis savo teisumo įrodinėjimas.",
            "Teisminiai konfliktai.",
            "Svetimų problemų sprendimas.",
        ],
        "Neįklimpkite į ginčus, teisumo įrodinėjimą ir svetimų problemų "
        "sprendimą. Atskirkit, už ką atsakote jūs, o už ką – kiti.",
    ),
    9: (
        "SAVIPAKANKAMUMAS",
        [
            "Užsidarymas savyje.",
            "Atsiribojimas nuo žmonių.",
            "Pagalbos atmetimas.",
            "Vienatvės pavertimas saugumo zona.",
        ],
        "Savipakankamumo nepaverskite izoliacija. "
        "Leiskite sau priimti kitų žmonių pagalbą ir artumą.",
    ),
    10: (
        "KARJEROS SIEKIS",
        [
            "Nuolatinis rezultatų vaikymasis.",
            "Statuso sureikšminimas.",
            "Nesugebėjimas sustoti pasiekus tikslą.",
            "Gyvenimo vertinimas tik pagal pasiekimus.",
        ],
        "Siekite rezultatų, tačiau neleiskite karjeros tikslams tapti "
        "vieninteliu jūsų gyvenimo matu.",
    ),
    11: (
        "DRAUGAI IR KONFLIKTAI",
        [
            "Įsitraukimas į draugų ir kitų žmonių konfliktus.",
            "Gelbėtojo vaidmuo.",
            "Bandymas išspręsti kitų žmonių problemas.",
            "Konfliktų prisiėmimas kaip savo.",
        ],
        "Neįsitraukite į svetimus konfliktus ir gelbėtojo vaidmenį. "
        "Atskirkite savo atsakomybę nuo kitų.",
    ),
    12: (
        "ASKETIZMAS",
        [
            "Savęs ribojimas.",
            "Aukos vaidmuo.",
            "Poreikių atsisakymas dėl kitų.",
            "Įsitikinimas, kad reikia kentėti ar aukotis.",
        ],
        "Nepaverskite savęs aukojimo gyvenimo būdu. "
        "Leiskite sau turėti poreikių, norų ir priimti gyvenimo teikiamas galimybes.",
    ),
    13: (
        "KRIZĖS",
        [
            "Gyvenimas nuolatinėmis krizėmis.",
            "Polinkis viską griauti ir pradėti iš naujo.",
            "Krizės kūrimas tam, kad atsirastų pokytis.",
            "Prisirišimas prie dramatiškų transformacijų.",
        ],
        "Pokyčiams nebūtina visko sugriauti. "
        "Mokykitės keisti gyvenimą sąmoningai, nelaukdami krizės.",
    ),
    14: (
        "NUOBODULYS",
        [
            "Stagnacija ir pasyvumas.",
            "Pokyčių vengimas.",
            "Įprastos rutinos laikymas vieninteliu saugumu.",
            "Gyvenimo atidėliojimas.",
        ],
        "Nepaverskite ramybės sąstingiu. "
        "Į gyvenimą sąmoningai įneškite judėjimo, naujų patirčių ir veiklos.",
    ),
    15: (
        "PRIKLAUSOMYBĖS",
        [
            "Prisirišimas prie žmonių.",
            "Emocinės priklausomybės.",
            "Materialinių malonumų sureikšminimas.",
            "Sunkumas atsisakyti to, kas jau kenkia.",
        ],
        "Stebėkite, kas pradeda jus valdyti. "
        "Mokykitės rinktis laisvai, o ne veikti iš priklausomybės ar prisirišimo.",
    ),
    16: (
        "GRIŪTIS",
        [
            "Polinkis viską nutraukti staiga.",
            "Savo gyvenimo struktūrų griovimas.",
            "Konfliktinis noras pradėti viską nuo nulio.",
            "Sprendimai emocinio sprogimo metu.",
        ],
        "Neskubėkite griauti to, ką galima pakeisti ar pertvarkyti. "
        "Pirmiausia įvertinkite, ką verta išsaugoti.",
    ),
    17: (
        "ILIUZIJOS",
        [
            "Idealizavimas.",
            "Gyvenimas ateities svajonėmis.",
            "Laukimas, kad viskas išsispręs savaime.",
            "Atitrūkimas nuo realių veiksmų.",
        ],
        "Svajones tikrinkite realiais veiksmais. "
        "Svarbu ne tik tikėti galimybe, bet ir konkrečiai judėti jos link.",
    ),
    18: (
        "UŽSIDARYMAS NAMUOSE",
        [
            "Atsiribojimas nuo išorinio pasaulio.",
            "Namų pavertimas vienintele saugia vieta.",
            "Baimė veikti išoriniame pasaulyje.",
            "Gyvenimas savo baimėmis ir abejonėmis.",
        ],
        "Namai gali būti jūsų atrama, bet ne slėptuvė nuo gyvenimo. "
        "Palaipsniui plėskite savo veikimo ir bendravimo erdvę.",
    ),
    19: (
        "ĮVAIZDIS IR ŠLOVĖ",
        [
            "Perdėtas poreikis būti pastebėtam.",
            "Priklausomybė nuo pripažinimo.",
            "Įvaizdžio sureikšminimas.",
            "Savivertės siejimas su kitų žmonių reakcijomis.",
        ],
        "Nevertinkite savęs tik pagal kitų dėmesį ar pripažinimą. "
        "Svarbiau reali jūsų vertė ir tai, ką kuriate.",
    ),
    20: (
        "VISUOMENĖ IR TEISĖ",
        [
            "Perdėtas įsitraukimas į visuomenės problemas.",
            "Kova už kitų teisybę savo sąskaita.",
            "Nuolatinis teisinių klausimų sprendimas.",
            "Savo gyvenimo nustūmimas dėl kolektyvinių reikalų.",
        ],
        "Dalyvaukite visuomeniniame gyvenime, tačiau nepamirškite savo "
        "asmeninių ribų, poreikių ir atsakomybės.",
    ),
    21: (
        "TRIUMFAS",
        [
            "Nuolatinis poreikis laimėti.",
            "Rezultato sureikšminimas.",
            "Nesugebėjimas priimti nesėkmės.",
            "Noras visada būti pirmam.",
        ],
        "Pergalė nėra vienintelis vertės matas. "
        "Vertinkite ir procesą, patirtį bei tai, ko išmokstate.",
    ),
    22: (
        "KELIONĖS IR LAISVĖ",
        [
            "Nuolatinis bėgimas nuo rutinos.",
            "Įsipareigojimų vengimas.",
            "Laisvės pavertimas vieninteliu tikslu.",
            "Sunkumas įsitvirtinti ir užbaigti pradėtus dalykus.",
        ],
        "Mėgaukitės laisve ir kelionėmis, tačiau nepaverskite jų būdu "
        "pabėgti nuo atsakomybės ir stabilumo.",
    ),
}


def mazinti_iki_22(skaicius):
    while skaicius > 22:
        skaicius -= 22
    return skaicius


def likimo_spastai(diena, menuo, metai):
    # Gimimo diena: jei > 22, atimame 22.
    dt = mazinti_iki_22(diena)

    # Metų skaitmenų suma.
    gt = sum(int(x) for x in str(metai))

    # Dt + Mt + Gt mažiname iki 22.
    bendra_suma = mazinti_iki_22(dt + menuo + gt)

    # Patvirtinta Likimo spąstų formulė:
    # Ls = ||Dt - Mt| - suma|
    rezultatas = abs(abs(dt - menuo) - bendra_suma)

    # Jei gaunamas 0, naudojame 22; jei >22 – mažiname.
    if rezultatas == 0:
        rezultatas = 22
    rezultatas = mazinti_iki_22(rezultatas)

    return rezultatas


def nuskaityti_data(tekstas):
    tekstas = tekstas.strip()

    match = re.fullmatch(
        r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})",
        tekstas,
    )

    if not match:
        return None

    diena, menuo, metai = map(int, match.groups())

    try:
        datetime(metai, menuo, diena)
    except ValueError:
        return None

    return diena, menuo, metai


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sveiki! 👋\n\n"
        "Įrašykite gimimo datą formatu:\n"
        "28.08.1974"
    )


async def skaiciuoti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = nuskaityti_data(update.message.text)

    if data is None:
        await update.message.reply_text(
            "Įrašykite gimimo datą formatu:\n"
            "28.08.1974"
        )
        return

    diena, menuo, metai = data
    rezultatas = likimo_spastai(diena, menuo, metai)

    pavadinimas, spastai, rekomendacija = ARKANAI[rezultatas]

    spastu_tekstas = "\n".join(f"• {punktas}" for punktas in spastai)

    atsakymas = (
        f"Rezultatas: {rezultatas}\n\n"
        f"{rezultatas} ARKANAS\n\n"
        f"{pavadinimas}\n\n"
        f"Spąstai:\n"
        f"{spastu_tekstas}\n\n"
        f"Rekomendacija:\n"
        f"{rekomendacija}"
    )

    await update.message.reply_text(atsakymas)


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN nerastas")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, skaiciuoti)
    )

    print("Botas paleistas.")
    app.run_polling()


if __name__ == "__main__":
    main()
