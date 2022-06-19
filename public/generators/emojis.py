from generator import EMOJIS

def generate( page, request):
    emojis = zip( EMOJIS[::3], EMOJIS[1::3], EMOJIS[2::3])

    emojis = "\n".join(f"<pre>{a}   {b}   {c}</pre>" for a,b,c in emojis)

    return page.replace("{EMOJI_LIST}", emojis)
