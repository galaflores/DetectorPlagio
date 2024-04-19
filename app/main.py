from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import LancasterStemmer
from nltk.util import ngrams
import re
import os
from gensim.models import Word2Vec
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import brown
from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() #lemmatizer algorithm
lancStemmer = LancasterStemmer() #stemming algorithm Lancaster

text1 = "Esta es una prueba. De los famosos n-gramas. Se esta usando NLTK. A diferencia de la detección de IA, que todavía es relativamente nueva y está evolucionando, la detección de plagio existe desde hace tiempo."
text2 = "Esta es otra prueba. Esto es para el ejercicio. Usando n-gramas en clase. A diferencia de una herramienta de IA, un periodista o redactor puede mantener conversaciones reales con expertos en la materia sobre la que escribe."

document = """I was jolted awake by the sound of gunfire in one of the neighboring stacks. The shots were followed by a few minutes of muffled shouting and screaming, then silence.

Gunfire wasn’t uncommon in the stacks, but it still shook me up. I knew I probably wouldn’t be able to fall back asleep, so I decided to kill the remaining hours until dawn by brushing up on a few coin-op classics. Galaga, Defender, Asteroids. These games were outdated digital dinosaurs that had become museum pieces long before I was born. But I was a gunter, so I didn’t think of them as quaint low-res antiques. To me, they were hallowed artifacts. Pillars of the pantheon. When I played the classics, I did so with a determined sort of reverence.

I was curled up in an old sleeping bag in the corner of the trailer’s tiny laundry room, wedged into the gap between the wall and the dryer. I wasn’t welcome in my aunt’s room across the hall, which was fine by me. I preferred to crash in the laundry room anyway. It was warm, it afforded me a limited amount of privacy, and the wireless reception wasn’t too bad. And, as an added bonus, the room smelled like liquid detergent and fabric softener. The rest of the trailer reeked of cat piss and abject poverty.

Most of the time I slept in my hideout. But the temperature had dropped below zero the past few nights, and as much as I hated staying at my aunt’s place, it still beat freezing to death.

A total of fifteen people lived in my aunt’s trailer. She slept in the smallest of its three bedrooms. The Depperts lived in the bedroom adjacent to her, and the Millers occupied the large master bedroom at the end of the hall. There were six of them, and they paid the largest share of the rent. Our trailer wasn’t as crowded as some of the other units in the stacks. It was a double-wide. Plenty of room for everybody.

I pulled out my laptop and powered it on. It was a bulky, heavy beast, almost ten years old. I’d found it in a Dumpster behind the abandoned strip mall across the highway. I’d been able to coax it back to life by replacing its system memory and reloading the stone-age operating system. The processor was slower than a sloth by current standards, but it was fine for my needs. The laptop served as my portable research library, video arcade, and home theater system. Its hard drive was filled with old books, movies, TV show episodes, song files, and nearly every videogame made in the twentieth century.

I booted up my emulator and selected Robotron: 2084, one of my all-time favorite games. I’d always loved its frenetic pace and brutal simplicity. Robotron was all about instinct and reflexes. Playing old videogames never failed to clear my mind and set me at ease. If I was feeling depressed or frustrated about my lot in life, all I had to do was tap the Player One button, and my worries would instantly slip away as my mind focused itself on the relentless pixelated onslaught on the screen in front of me. There, inside the game’s two-dimensional universe, life was simple: It’s just you against the machine. Move with your left hand, shoot with your right, and try to stay alive as long as possible.

I spent a few hours blasting through wave after wave of Brains, Spheroids, Quarks, and Hulks in my unending battle to Save the Last Human Family! But eventually my fingers started to cramp up and I began to lose my rhythm. When that happened at this level, things deteriorated quickly. I burned through all of my extra lives in a matter of minutes, and my two least-favorite words appeared on the screen: game over.

I shut down the emulator and began to browse through my video files. Over the past five years, I’d downloaded every single movie, TV show, and cartoon mentioned in Anorak’s Almanac. I still hadn’t watched all of them yet, of course. That would probably take decades.

I selected an episode of Family Ties, an ’80s sitcom about a middle-class family living in central Ohio. I’d downloaded the show because it had been one of Halliday’s favorites, and I figured there was a chance that some clue related to the Hunt might be hidden in one of the episodes. I’d become addicted to the show immediately, and had now watched all 180 episodes, multiple times. I never seemed to get tired of them.

Sitting alone in the dark, watching the show on my laptop, I always found myself imagining that I lived in that warm, well-lit house, and that those smiling, understanding people were my family. That there was nothing so wrong in the world that we couldn’t sort it out by the end of a single half-hour episode (or maybe a two-parter, if it was something really serious).

My own home life had never even remotely resembled the one depicted in Family Ties, which was probably why I loved the show so much. I was the only child of two teenagers, both refugees who’d met in the stacks where I’d grown up. I don’t remember my father. When I was just a few months old, he was shot dead while looting a grocery store during a power blackout. The only thing I really knew about him was that he loved comic books. I’d found several old flash drives in a box of his things, containing complete runs of The Amazing Spider-Man, The X-Men, and Green Lantern. My mom once told me that my dad had given me an alliterative name, Wade Watts, because he thought it sounded like the secret identity of a superhero. Like Peter Parker or Clark Kent. Knowing that made me think he was must have been a cool guy, despite how he’d died.

My mother, Loretta, had raised me on her own. We’d lived in a small RV in another part of the stacks. She had two full-time OASIS jobs, one as a telemarketer, the other as an escort in an online brothel. She used to make me wear earplugs at night so I wouldn’t hear her in the next room, talking dirty to tricks in other time zones. But the earplugs didn’t work very well, so I would watch old movies instead, with the volume turned way up.

I was introduced to the OASIS at an early age, because my mother used it as a virtual babysitter. As soon as I was old enough to wear a visor and a pair of haptic gloves, my mom helped me create my first OASIS avatar. Then she stuck me in a corner and went back to work, leaving me to explore an entirely new world, very different from the one I’d known up until then.

From that moment on, I was more or less raised by the OASIS’s interactive educational programs, which any kid could access for free. I spent a big chunk of my childhood hanging out in a virtual-reality simulation of Sesame Street, singing songs with friendly Muppets and playing interactive games that taught me how to walk, talk, add, subtract, read, write, and share. Once I’d mastered those skills, it didn’t take me long to discover that the OASIS was also the world’s biggest public library, where even a penniless kid like me had access to every book ever written, every song ever recorded, and every movie, television show, videogame, and piece of artwork ever created. The collected knowledge, art, and amusements of all human civilization were there, waiting for me. But gaining access to all of that information turned out to be something of a mixed blessing. Because that was when I found out the truth.

...

I don’t know, maybe your experience differed from mine. For me, growing up as a human being on the planet Earth in the twenty-first century was a real kick in the teeth. Existentially speaking.

The worst thing about being a kid was that no one told me the truth about my situation. In fact, they did the exact opposite. And, of course, I believed them, because I was just a kid and I didn’t know any better. I mean, Christ, my brain hadn’t even grown to full size yet, so how could I be expected to know when the adults were bullshitting me?

So I swallowed all of the dark ages nonsense they fed me. Some time passed. I grew up a little, and I gradually began to figure out that pretty much everyone had been lying to me about pretty much everything since the moment I emerged from my mother’s womb.

This was an alarming revelation.

It gave me trust issues later in life.

I started to figure out the ugly truth as soon as I began to explore the free OASIS libraries. The facts were right there waiting for me, hidden in old books written by people who weren’t afraid to be honest. Artists and scientists and philosophers and poets, many of them long dead. As I read the words they’d left behind, I finally began to get a grip on the situation. My situation. Our situation. What most people referred to as “the human condition.”

It was not good news.

I wish someone had just told me the truth right up front, as soon as I was old enough to understand it. I wish someone had just said:

“Here’s the deal, Wade. You’re something called a ‘human being.’ That’s a really smart kind of animal. Like every other animal on this planet, we’re descended from a single-celled organism that lived millions of years ago. This happened by a process called evolution, and you’ll learn more about it later. But trust me, that’s really how we all got here. There’s proof of it everywhere, buried in the rocks. That story you heard? About how we were all created by a super-powerful dude named God who lives up in the sky? Total bullshit. The whole God thing is actually an ancient fairy tale that people have been telling to one another for thousands of years. We made it all up. Like Santa Claus and the Easter Bunny.

“Oh, and by the way . . .​ there’s no Santa Claus or Easter Bunny. Also bullshit. Sorry, kid. Deal with it.

“You’re probably wondering what happened before you got here. An awful lot of stuff, actually. Once we evolved into humans, things got pretty interesting. We figured out how to grow food and domesticate animals so we didn’t have to spend all of our time hunting. Our tribes got much bigger, and we spread across the entire planet like an unstoppable virus. Then, after fighting a bunch of wars with each other over land, resources, and our made-up gods, we eventually got all of our tribes organized into a ‘global civilization.’ But, honestly, it wasn’t all that organized, or civilized, and we continued to fight a lot of wars with each other. But we also figured out how to do science, which helped us develop technology. For a bunch of hairless apes, we’ve actually managed to invent some pretty incredible things. Computers. Medicine. Lasers. Microwave ovens. Artificial hearts. Atomic bombs. We even sent a few guys to the moon and brought them back. We also created a global communications network that lets us all talk to each other, all around the world, all the time. Pretty impressive, right?

“But that’s where the bad news comes in. Our global civilization came at a huge cost. We needed a whole bunch of energy to build it, and we got that energy by burning fossil fuels, which came from dead plants and animals buried deep in the ground. We used up most of this fuel before you got here, and now it’s pretty much all gone. This means that we no longer have enough energy to keep our civilization running like it was before. So we’ve had to cut back. Big-time. We call this the Global Energy Crisis, and it’s been going on for a while now.

“Also, it turns out that burning all of those fossil fuels had some nasty side effects, like raising the temperature of our planet and screwing up the environment. So now the polar ice caps are melting, sea levels are rising, and the weather is all messed up. Plants and animals are dying off in record numbers, and lots of people are starving and homeless. And we’re still fighting wars with each other, mostly over the few resources we have left.

“Basically, kid, what this all means is that life is a lot tougher than it used to be, in the Good Old Days, back before you were born. Things used to be awesome, but now they’re kinda terrifying. To be honest, the future doesn’t look too bright. You were born at a pretty crappy time in history. And it looks like things are only gonna get worse from here on out. Human civilization is in ‘decline.’ Some people even say it’s ‘collapsing.’

“You’re probably wondering what’s going to happen to you. That’s easy. The same thing is going to happen to you that has happened to every other human being who has ever lived. You’re going to die. We all die. That’s just how it is.

“What happens when you die? Well, we’re not completely sure. But the evidence seems to suggest that nothing happens. You’re just dead, your brain stops working, and then you’re not around to ask annoying questions anymore. Those stories you heard? About going to a wonderful place called ‘heaven’ where there is no more pain or death and you live forever in a state of perpetual happiness? Also total bullshit. Just like all that God stuff. There’s no evidence of a heaven and there never was. We made that up too. Wishful thinking. So now you have to live the rest of your life knowing you’re going to die someday and disappear forever.

“Sorry.”

...

OK, on second thought, maybe honesty isn’t the best policy after all. Maybe it isn’t a good idea to tell a newly arrived human being that he’s been born into a world of chaos, pain, and poverty just in time to watch everything fall to pieces. I discovered all of that gradually over several years, and it still made me feel like jumping off a bridge.

Luckily, I had access to the OASIS, which was like having an escape hatch into a better reality. The OASIS kept me sane. It was my playground and my preschool, a magical place where anything was possible.

The OASIS is the setting of all my happiest childhood memories. When my mom didn’t have to work, we would log in at the same time and play games or go on interactive storybook adventures together. She used to have to force me to log out every night, because I never wanted to return to the real world. Because the real world sucked.

I never blamed my mom for the way things were. She was a victim of fate and cruel circumstance, like everyone else. Her generation had it the hardest. She’d been born into a world of plenty, then had to watch it all slowly vanish. More than anything, I remember feeling sorry for her. She was depressed all the time, and taking drugs seemed to be the only thing she truly enjoyed. Of course, they were what eventually killed her. When I was eleven years old, she shot a bad batch of something into her arm and died on our ratty fold-out sofa bed while listening to music on an old mp3 player I’d repaired and given to her the previous Christmas."""

def get_stemmer(text):
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    nueva = lancStemmer.stem(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto

def get_lemm(text):
  palabras = [palabra.lower() for palabra in re.findall(r'\w+', text.lower())]
  text_lista = []
  for palabra in palabras:
    nueva = lemmatizer.lemmatize(palabra)
    text_lista.append(nueva)
  nuevo_texto = ' '.join(text_lista)
  return nuevo_texto


def get_grams(text, n):
  text = get_stemmer(text) #pre-procesa el parrafo
  text = re.findall(r"\w+", text) #separa los caracteres pre-procesados del parrafo en listas
  grams = ngrams(text,n) #genera los ngrams
  result = []
  for ng in grams:
    result.append(' '.join(ng)) #agrega los ngrams en una lista llamada result
  return result

def matriz_parrafos(gramas1, gramas2):
  grams_palabras = set(gramas1 + gramas2) #set de palabras de ambos ngrams
  grams_juntos = [gramas1, gramas2] #lista con ambas listas de los ngrams de cada parrafo
  matriz = []
  for grama in grams_juntos:
    vector = []
    for palabra in grams_palabras:
      vector.append(1 if palabra in grama else 0) #compara las palabras de los grams a la palabra y agrega o un 1 o un 0 al vector del parrafo
    matriz.append(vector)
  return matriz

def cargar_docs(ruta):
  with open(ruta, 'r') as file:
    return file.read()

def similitud_documento(doc1, doc2):
    unigrams_doc1 = get_grams(doc1, 1)
    bigrams_doc1 = get_grams(doc1, 2)
    trigrams_doc1 = get_grams(doc1, 3)

    unigrams_doc2 = get_grams(doc2, 1)
    bigrams_doc2 = get_grams(doc2, 2)
    trigrams_doc2 = get_grams(doc2, 3)

    similitud_unigrams = cosine_similarity(matriz_parrafos(unigrams_doc1, unigrams_doc2))
    similitud_bigrams = cosine_similarity(matriz_parrafos(bigrams_doc1, bigrams_doc2))
    similitud_trigrams = cosine_similarity(matriz_parrafos(trigrams_doc1, trigrams_doc2))

    print("Similitud de coseno (unigrams) entre doc1 y doc2:", similitud_unigrams[0][1])
    print("Similitud de coseno (bigrams) entre doc1 y doc2:", similitud_bigrams[0][1])
    print("Similitud de coseno (trigrams) entre doc1 y doc2:", similitud_trigrams[0][1])

ruta_docs = "dos_org"
doc1 = cargar_docs(os.path.join(ruta_docs, "documento_org1.txt"))
doc2 = cargar_docs(os.path.join(ruta_docs, "documento_org2.txt"))

similitud_documento(doc1, doc2)