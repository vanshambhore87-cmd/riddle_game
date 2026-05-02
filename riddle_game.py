import streamlit as st
import random
import time

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(page_title="Riddle Master", page_icon="🧩", layout="centered")

# =========================================
# THE OFFLINE DATABASE (Add your 100+ here!)
# =========================================
RIDDLES_DB = {
        "English": [
        {"riddle": "What has to be broken before you can use it?", "answer": "egg", "hint": "Often eaten for breakfast."},
        {"riddle": "I am full of holes but still hold water. What am I?", "answer": "sponge", "hint": "Used for washing dishes."},
        {"riddle": "What month of the year has 28 days?", "answer": "all", "hint": "Every single one of them."},
        {"riddle": "What is always in front of you but can’t be seen?", "answer": "future", "hint": "Tomorrow and beyond."},
        {"riddle": "What can you break, even if you never pick it up or touch it?", "answer": "promise", "hint": "A sworn word."},
        {"riddle": "What gets bigger the more you take away?", "answer": "hole", "hint": "You dig it in the ground."},
        {"riddle": "I shave every day, but my beard stays the same. What am I?", "answer": "barber", "hint": "Cuts other people's hair."},
        {"riddle": "What has words, but never speaks?", "answer": "book", "hint": "You read it in a library."},
        {"riddle": "What can you catch, but not throw?", "answer": "cold", "hint": "Makes you sneeze and cough."},
        {"riddle": "What has many rings but no fingers?", "answer": "tree", "hint": "Look at its wooden stump."},
        {"riddle": "What has four legs but can't walk?", "answer": "table", "hint": "You eat your dinner on it."},
        {"riddle": "What runs all around a backyard, yet never moves?", "answer": "fence", "hint": "Keeps the dog inside."},
        {"riddle": "What has a bottom at the top?", "answer": "legs", "hint": "Body parts you stand on."},
        {"riddle": "What has a neck but no head?", "answer": "bottle", "hint": "Holds water or soda."},
        {"riddle": "I have a single eye but cannot see.", "answer": "needle", "hint": "Used with thread to sew clothes."},
        {"riddle": "What belongs to you, but other people use it more than you?", "answer": "name", "hint": "What people call you."},
        {"riddle": "What kind of band never plays music?", "answer": "rubber", "hint": "Stretchy and holds things together."},
        {"riddle": "What has many teeth, but cannot bite?", "answer": "comb", "hint": "Used on your hair."},
        {"riddle": "What building has the most stories?", "answer": "library", "hint": "Filled with books."},
        {"riddle": "I have cities, but no houses. I have mountains, but no trees.", "answer": "map", "hint": "Used for navigation."},
        {"riddle": "What drops but never crashes?", "answer": "temperature", "hint": "Makes the weather colder."},
        {"riddle": "What tastes better than it smells?", "answer": "tongue", "hint": "A muscle inside your mouth."},
        {"riddle": "I am an odd number. Take away a letter and I become even.", "answer": "seven", "hint": "The number after six."},
        {"riddle": "If you’ve got me, you want to share me; if you share me, you haven’t kept me.", "answer": "secret", "hint": "Shhh! Don't tell anyone."},
        {"riddle": "What goes through cities and fields, but never moves?", "answer": "road", "hint": "Cars drive on it."},
        {"riddle": "I am not alive, but I grow; I don't have lungs, but I need air.", "answer": "fire", "hint": "Hot, bright, and burns."},
        {"riddle": "What is easy to get into, but hard to get out of?", "answer": "trouble", "hint": "When you do something bad."},
        {"riddle": "What goes up and down but doesn't move?", "answer": "stairs", "hint": "You walk on them to go to the next floor."},
        {"riddle": "What begins with an E and only contains one letter?", "answer": "envelope", "hint": "You put mail inside it."},
        {"riddle": "The more you take, the more you leave behind. What are they?", "answer": "footsteps", "hint": "Tracks on the ground."},
        {"riddle": "I have keys but no locks. I have a space but no room.", "answer": "keyboard", "hint": "You type on it."},
        {"riddle": "What can travel around the world while staying in a corner?", "answer": "stamp", "hint": "Put on a letter for the post office."},
        {"riddle": "What is always coming but never arrives?", "answer": "tomorrow", "hint": "The day after today."},
        {"riddle": "What has 13 hearts, but no other organs?", "answer": "deck", "hint": "Used to play card games."},
        {"riddle": "I am white when I am dirty, and black when I am clean.", "answer": "chalkboard", "hint": "Used in classrooms."},
        {"riddle": "What starts with a P, ends with an E, and has thousands of letters?", "answer": "postoffice", "hint": "The place that sends your mail."},
        {"riddle": "What loses its head in the morning and gets it back at night?", "answer": "pillow", "hint": "You rest your head on it in bed."},
        {"riddle": "What is so fragile that saying its name breaks it?", "answer": "silence", "hint": "Absolute quiet."},
        {"riddle": "What runs but never walks, murmurs but never talks?", "answer": "river", "hint": "Flowing water in nature."},
        {"riddle": "I can fly without wings. I can cry without eyes.", "answer": "cloud", "hint": "Floats in the sky and makes rain."},
        {"riddle": "What gets sharper the more you use it?", "answer": "brain", "hint": "The organ inside your head."},
        {"riddle": "If you drop me I’m sure to crack, but give me a smile and I’ll always smile back.", "answer": "mirror", "hint": "Shows your reflection."},
        {"riddle": "I follow you all the time and copy your every move, but you can’t touch me.", "answer": "shadow", "hint": "Made by the sun blocking your body."},
        {"riddle": "What kind of room has no doors or windows?", "answer": "mushroom", "hint": "A fungus that grows in the wild."},
        {"riddle": "What can fill a room but takes up no space?", "answer": "light", "hint": "Comes from a bulb or the sun."},
        {"riddle": "Which letter of the alphabet has the most water?", "answer": "c", "hint": "Sounds like the ocean."},
        {"riddle": "What starts with T, ends with T, and has T in it?", "answer": "teapot", "hint": "Pours a hot drink."},
        {"riddle": "Where does today come before yesterday?", "answer": "dictionary", "hint": "A book of words in alphabetical order."},
        {"riddle": "I have a tail and a head, but no body. What am I?", "answer": "coin", "hint": "You flip it to make a decision."},
        {"riddle": "What has to be broken before you can eat it?", "answer": "coconut", "hint": "A hard tropical fruit with water inside."}
    ],

        "Hindi": [
        {"riddle": "काला घोड़ा, सफेद सवारी, एक उतरा तो दूसरे की बारी।", "answer": "तवा", "hint": "रोटी बनाने के काम आता है।"},
        {"riddle": "एक फूल काले रंग का, सिर पर हमेशा सुहाए।", "answer": "छतरी", "hint": "बारिश में काम आती है।"},
        {"riddle": "कटोरी पे कटोरी, बेटा बाप से भी गोरा।", "answer": "प्याज", "hint": "काटते समय आंसू आते हैं।"},
        {"riddle": "लाल पूंछ हरी बिलाई, इसका हल बता मेरे भाई।", "answer": "मूली", "hint": "यह एक सफेद सब्जी/सलाद है।"},
        {"riddle": "बीमार नहीं रहती, फिर भी खाती है गोली।", "answer": "बंदूक", "hint": "सैनिक इसका इस्तेमाल करते हैं।"},
        {"riddle": "हरी डिब्बी, पीला मकान, उसमें बैठे कल्लू राम।", "answer": "पपीता", "hint": "एक मीठा फल है जिसके बीज काले होते हैं।"},
        {"riddle": "बिना बुलाए डॉक्टर आए, सूई लगाकर फुर्र हो जाए।", "answer": "मच्छर", "hint": "रात को सोने नहीं देता।"},
        {"riddle": "पैर नहीं पर चलती है, कभी न राह भटकती है।", "answer": "घड़ी", "hint": "समय बताती है।"},
        {"riddle": "तीन अक्षर का मेरा नाम, उलटा सीधा एक समान।", "answer": "नयन", "hint": "आंख का पर्यायवाची शब्द।"},
        {"riddle": "सुबह आए, शाम को जाए, दुनिया भर की खबर लाए।", "answer": "अखबार", "hint": "हम इसे रोज पढ़ते हैं।"},
        {"riddle": "सोने को पलंग नहीं, न महल बनाए, एक रुपया पास नहीं, फिर भी राजा कहलाए।", "answer": "शेर", "hint": "जंगल का मुखिया।"},
        {"riddle": "पानी मेरा बाप, पानी ही मेरा बेटा, मुंह ऊपर करके देखो मैं सबके ऊपर लेटा।", "answer": "बादल", "hint": "बारिश लाता है।"},
        {"riddle": "छोटा सा सिपाही, खींच के उसकी पैंट उतारी।", "answer": "केला", "hint": "एक पीला फल।"},
        {"riddle": "हरी डंडी, लाल कमान, तौबा तौबा करे इंसान।", "answer": "मिर्च", "hint": "खाने में बहुत तीखी होती है।"},
        {"riddle": "एक घर में चालीस चोर, सबका मुंह है काला।", "answer": "माचिस", "hint": "आग लगाने के काम आती है।"},
        {"riddle": "बिन पंख के उड़े आकाश, लंबी पूंछ हमारे पास।", "answer": "पतंग", "hint": "मकर संक्रांति पर उड़ाते हैं।"},
        {"riddle": "आठ पैर और दो हैं हाथ, जाला बुनना इसका काम।", "answer": "मकड़ी", "hint": "दीवारों पर जाला बनाती है।"},
        {"riddle": "लंबी पूंछ, पीठ पर कूबड़, रेगिस्तान का है यह जहाज।", "answer": "ऊंट", "hint": "रेगिस्तान में पाया जाता है।"},
        {"riddle": "दिन में सोए, रात में रोए, जितना रोए उतना खोए।", "answer": "मोमबत्ती", "hint": "बिजली जाने पर जलाते हैं।"},
        {"riddle": "चार पैर हैं पर चल नहीं सकती।", "answer": "मेज", "hint": "इस पर रखकर खाना खाते हैं या पढ़ते हैं।"},
        {"riddle": "सफेद रंग का मेरा शरीर, समुद्र से मेरा जन्म।", "answer": "नमक", "hint": "खाने का स्वाद बढ़ाता है।"},
        {"riddle": "गोल है पर गेंद नहीं, रोशनी दे पर सूरज नहीं।", "answer": "बल्ब", "hint": "कमरे में उजाला करता है।"},
        {"riddle": "जितना पास जाओगे, उतना कम दिखेगा।", "answer": "कोहरा", "hint": "सर्दियों की सुबह में होता है।"},
        {"riddle": "मुँह नहीं पर बोलता है, दुनिया की खबर सुनाता है।", "answer": "रेडियो", "hint": "गाने और समाचार सुनाता है।"},
        {"riddle": "एक पेड़ पर पांच पत्ते, न कोई फल न कोई फूल।", "answer": "हाथ", "hint": "हमारे शरीर का हिस्सा है।"},
        {"riddle": "बिना तेल के जलता है, सारे जग को रोशन करता है।", "answer": "सूरज", "hint": "दिन में आसमान में चमकता है।"},
        {"riddle": "मुझसे कोई बच नहीं सकता, धूप में साथ चलती हूँ।", "answer": "परछाई", "hint": "रोशनी में आपके पीछे या आगे होती है।"},
        {"riddle": "न हाथ हैं, न पैर हैं, फिर भी रेंगता है।", "answer": "सांप", "hint": "जहरीला होता है और फन फैलाता है।"},
        {"riddle": "रात को आते हैं, दिन में छिप जाते हैं।", "answer": "तारे", "hint": "आसमान में टिमटिमाते हैं।"},
        {"riddle": "जो कभी वापस नहीं आता।", "answer": "समय", "hint": "घड़ी में आगे बढ़ता रहता है।"},
        {"riddle": "ऐसा क्या है जिसे काटने पर लोग गाना गाते हैं?", "answer": "केक", "hint": "जन्मदिन पर काटते हैं।"},
        {"riddle": "जिसे हम देख सकते हैं पर छू नहीं सकते।", "answer": "सपना", "hint": "नींद में आता है।"},
        {"riddle": "लाल है पर टमाटर नहीं, बहता है पर पानी नहीं।", "answer": "खून", "hint": "शरीर के अंदर होता है।"},
        {"riddle": "ऐसी कौन सी चीज है जो ऊपर जाती है पर नीचे नहीं आती?", "answer": "उम्र", "hint": "हर साल बढ़ती है।"},
        {"riddle": "जिसके पास गला है पर सिर नहीं।", "answer": "बोतल", "hint": "इसमें पानी रखते हैं।"},
        {"riddle": "काले हैं पर काग नहीं, लंबे हैं पर नाग नहीं।", "answer": "बाल", "hint": "सिर पर उगते हैं।"},
        {"riddle": "दो अक्षर का मेरा नाम, आता हूँ खाने के काम।", "answer": "सेब", "hint": "एक लाल रंग का फल।"},
        {"riddle": "गोल-गोल चेहरा, पेट में बहुत सारे लाल दाने।", "answer": "अनार", "hint": "एक मीठा और रसदार फल।"},
        {"riddle": "एक किले के दो ही द्वार, उनमें सैनिक सफेद दार।", "answer": "मुंह", "hint": "खाना खाने के काम आता है।"},
        {"riddle": "गर्मी में आता हूँ, ठंड में छिप जाता हूँ, मेरा नाम बताओ।", "answer": "पसीना", "hint": "कड़ी मेहनत के बाद निकलता है।"},
        {"riddle": "वह क्या है जो टूटने के बाद ही काम आता है?", "answer": "अंडा", "hint": "मुर्गी देती है।"},
        {"riddle": "मैं सबके पास हूँ, पर कोई मुझे खोना नहीं चाहता।", "answer": "जिंदगी", "hint": "जीवन का दूसरा नाम।"},
        {"riddle": "एक ऐसा कमरा जिसमें कोई खिड़की या दरवाजा नहीं होता।", "answer": "मशरूम", "hint": "एक प्रकार की खाने वाली फफूंद।"},
        {"riddle": "वह कौन है जो पूरे घर में घूमती है पर कोने में खड़ी रहती है?", "answer": "झाड़ू", "hint": "सफाई के काम आती है।"},
        {"riddle": "सफेद खेत, काले बीज, जो बोए वह बड़ा चतुर।", "answer": "किताब", "hint": "पढ़ाई करने के लिए होती है।"},
        {"riddle": "जितना सुखाओ, उतना ही गीला हो जाता है।", "answer": "तौलिया", "hint": "नहाने के बाद इस्तेमाल करते हैं।"},
        {"riddle": "दांत हैं पर काटता नहीं।", "answer": "कंघी", "hint": "बाल संवारने के काम आती है।"},
        {"riddle": "आंखें हैं पर देख नहीं सकता, पैर हैं पर चल नहीं सकता।", "answer": "गुड़िया", "hint": "बच्चों के खेलने का खिलौना।"},
        {"riddle": "वह क्या है जो तुम्हारे पास है, पर इस्तेमाल दूसरे करते हैं?", "answer": "नाम", "hint": "तुम्हारी पहचान।"},
        {"riddle": "कान मरोड़ो तो आगे बढ़ती है।", "answer": "साइकिल", "hint": "इसमें दो पहिए होते हैं।"}
    ],

        "Marathi": [
        {"riddle": "लाल गाय लाकूड खाय, पाणी पिताच मरून जाय.", "answer": "आग", "hint": "हिवाळ्यात शेकोटी करण्यासाठी लावतात."},
        {"riddle": "एक पाय आणि डोक्यावर टोपी.", "answer": "छत्री", "hint": "पावसापासून वाचवते."},
        {"riddle": "पंख नाहीत पण उडते, शेपूट नाही पण वळते.", "answer": "पतंग", "hint": "मकर संक्रांतीला आकाशात दिसते."},
        {"riddle": "दात आहेत पण चावत नाही.", "answer": "कंगवा", "hint": "केस विंचरण्यासाठी वापरतात."},
        {"riddle": "चार पाय आहेत पण चालू शकत नाही.", "answer": "टेबल", "hint": "अभ्यास करण्यासाठी यावर पुस्तके ठेवतात."},
        {"riddle": "डोके कापले तरी रडत नाही, उलट आपणच रडतो.", "answer": "कांदा", "hint": "भाजीत टाकतात, चिरताना डोळ्यात पाणी येते."},
        {"riddle": "आतून पांढरा, बाहेरून हिरवा, खायला लागतो गोड.", "answer": "पेरू", "hint": "पोपटाचे आवडते फळ."},
        {"riddle": "कितीही खाल्ली तरी पोट भरत नाही.", "answer": "शप्पथ", "hint": "खरे बोलण्यासाठी लोक घेतात."},
        {"riddle": "मान आहे पण डोके नाही, हात आहेत पण बोटे नाहीत.", "answer": "शर्ट", "hint": "अंगात घालण्याचे एक वस्त्र."},
        {"riddle": "पाण्यात जन्मते, पाण्यातच मरते.", "answer": "मीठ", "hint": "याशिवाय जेवणाला चव येत नाही."},
        {"riddle": "काळी आहे पण कावळा नाही, लांब आहे पण साप नाही.", "answer": "वेणी", "hint": "स्त्रिया केसांची घालतात."},
        {"riddle": "दोन भाऊ नेहमी एकत्र राहतात, पण एकमेकांना कधीच पाहत नाहीत.", "answer": "डोळे", "hint": "आपल्याला जग दाखवतात."},
        {"riddle": "जेवढा जास्त असतो, तेवढे कमी दिसते.", "answer": "अंधार", "hint": "रात्री होतो."},
        {"riddle": "फाटते पण आवाज येत नाही.", "answer": "दूध", "hint": "लिंबू पिळल्यावर असे होते."},
        {"riddle": "कुंभार नाही पण मडकी घडवतो, शिंपी नाही पण पाने शिवतो.", "answer": "सुगरण", "hint": "एक पक्षी जो सुंदर घरटे बांधतो."},
        {"riddle": "उजेडात सोबत असते, अंधारात गायब होते.", "answer": "सावली", "hint": "तुमच्या पावलावर पाऊल ठेवून चालते."},
        {"riddle": "एक घर ज्याला दरवाजे नाहीत.", "answer": "अंडे", "hint": "यातून पिल्लू बाहेर येते."},
        {"riddle": "गोड आहे पण खाता येत नाही.", "answer": "आवाज", "hint": "गायकाचा असतो."},
        {"riddle": "बाहेरून काटे, आतून गोड.", "answer": "फणस", "hint": "कोकणात मिळणारे एक मोठे फळ."},
        {"riddle": "जंगलात जन्मते, घरात रडते.", "answer": "बासरी", "hint": "श्रीकृष्ण वाजवत असे."},
        {"riddle": "पाणी पिल्यास मरते.", "answer": "तहान", "hint": "उन्हाळ्यात खूप लागते."},
        {"riddle": "हात पाय नाहीत, तरीही ती पळते.", "answer": "हवा", "hint": "आपल्याला श्वास घेण्यासाठी लागते."},
        {"riddle": "एका खोलीत अनेक माणसे, सर्वांच्या डोक्यावर लाल टोप्या.", "answer": "काडीपेटी", "hint": "आग लावण्यासाठी वापरतात."},
        {"riddle": "एकच डोळा आहे पण पाहू शकत नाही.", "answer": "सुई", "hint": "कपडे शिवण्यासाठी वापरतात."},
        {"riddle": "वर जाते पण खाली येत नाही.", "answer": "वय", "hint": "दर वाढदिवसाला वाढते."},
        {"riddle": "तोंड नाही पण शिट्टी वाजवते.", "answer": "कुकर", "hint": "स्वयंपाकघरात भात शिजवताना आवाज येतो."},
        {"riddle": "पांढरा हत्ती, हिरवी शेपटी.", "answer": "मुळा", "hint": "पांढऱ्या रंगाची भाजी / कोशिंबीर."},
        {"riddle": "लाल लाल डबीत, पांढरे पांढरे खडे.", "answer": "डाळिंब", "hint": "लाल रंगाचे गोड फळ."},
        {"riddle": "हात नाहीत, पाय नाहीत, तरीही दार उघडते.", "answer": "वारा", "hint": "जोराने आला की खिडक्या वाजतात."},
        {"riddle": "रस्ता आहे पण गाड्या नाहीत, शहरे आहेत पण घरे नाहीत.", "answer": "नकाशा", "hint": "भूगोलाच्या पुस्तकात असतो."},
        {"riddle": "चालत जाते पण पाऊलखुणा सोडत नाही.", "answer": "बोट", "hint": "पाण्यावर चालते."},
        {"riddle": "तीन अक्षरी माझे नाव, उलटे वाचले तरी तेच नाव.", "answer": "नमन", "hint": "नमस्कार करण्याचा एक शब्द."},
        {"riddle": "डोळे नाहीत पण रडतो.", "answer": "ढग", "hint": "पावसाळ्यात आकाशात काळे दिसतात."},
        {"riddle": "पाय नाहीत तरीही चालते.", "answer": "घड्याळ", "hint": "वेळ दाखवते."},
        {"riddle": "घरात येतो पण दार उघडत नाही.", "answer": "उजेड", "hint": "सकाळी सूर्याकडून मिळतो."},
        {"riddle": "रंगाने काळा, पण काम करतो उजेडाचे.", "answer": "कोळसा", "hint": "जाळल्यावर उष्णता देतो."},
        {"riddle": "स्वतः जळते पण इतरांना प्रकाश देते.", "answer": "मेणबत्ती", "hint": "लाईट गेल्यावर लावतात."},
        {"riddle": "एक पायरी चढायला पूर्ण दिवस लागतो.", "answer": "तारीख", "hint": "कॅलेंडरमध्ये रोज बदलते."},
        {"riddle": "जेवढी पुसाल तेवढी ती काळी होते.", "answer": "पाटी", "hint": "लहान मुले यावर लिहितात."},
        {"riddle": "अंगभर डोळे, तरीही आंधळा.", "answer": "जाळे", "hint": "कोळी घराच्या कोपऱ्यात बनवतो."},
        {"riddle": "लहानशी डबी, त्यात खडीसाखर.", "answer": "दात", "hint": "अन्न चावण्यासाठी लागतात."},
        {"riddle": "पांढरे शेत, काळे बी, जो पेरेल तोच शहाणा.", "answer": "पुस्तक", "hint": "वाचनासाठी वापरतात."},
        {"riddle": "ओळख पाहू मी कोण? पाय नाहीत पण चालतो, तोंड नाही पण बोलतो.", "answer": "रुपया", "hint": "खिशात वाजतो (पैसे)."},
        {"riddle": "आईच्या गळ्यात मोत्याचा हार, पोरगं रडतंय वारंवार.", "answer": "जाते", "hint": "धान्य दळण्यासाठी जुने साधन."},
        {"riddle": "जन्मतःच तिला कपडे नसतात, पण मोठी होताच कपडे घालते.", "answer": "कणीस", "hint": "मक्याचे असते, भाजून खातात."},
        {"riddle": "आकाशातून पडली पांढरी राणी, जमिनीवर पडताच झाले पाणी.", "answer": "गार", "hint": "पावसाळ्यात पडणारा बर्फ."},
        {"riddle": "काटे आहेत पण झाड नाही, पाने आहेत पण फांदी नाही.", "answer": "पुस्तक", "hint": "शाळेत बॅगेत असते."},
        {"riddle": "सर्वांकडे असते, पण कोणीही देऊ शकत नाही.", "answer": "नाव", "hint": "लोक तुम्हाला याने हाक मारतात."},
        {"riddle": "कानात घालतात पण दागिना नाही.", "answer": "कापूस", "hint": "पांढऱ्या रंगाचा आणि मऊ असतो."},
        {"riddle": "दोन भाऊ शेजारी, भेट नाही संसारी.", "answer": "डोळे", "hint": "आपण यातून पाहतो."}
    ],

# =========================================
# SESSION STATE DEFAULTS
# =========================================
defaults = {
    "language": None,
    "streak": 0,
    "high_score": 0,
    "current_riddle": "",
    "real_answer": "",
    "lives": 3,
    "hint": "",
    "show_next": False,
    "status_msg": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================
# GAME ENGINE FUNCTIONS
# =========================================
def load_new_riddle():
    # Pick a random riddle from the chosen language list!
    chosen_riddle = random.choice(RIDDLES_DB[st.session_state.language])
    
    st.session_state.current_riddle = chosen_riddle["riddle"]
    st.session_state.real_answer = chosen_riddle["answer"]
    # We load the hint instantly but hide it until they click the button
    st.session_state.hidden_hint = chosen_riddle["hint"] 
    
    st.session_state.hint = ""
    st.session_state.lives = 3
    st.session_state.show_next = False
    st.session_state.status_msg = ""

# =========================================
# LANGUAGE SELECTOR UI
# =========================================
if st.session_state.language is None:
    st.title("🧩 Riddle Master")
    st.subheader("Choose your language")
    c1, c2, c3 = st.columns(3)
    if c1.button("🇺🇸 English", use_container_width=True):
        st.session_state.language = "English"
        st.rerun()
    if c2.button("🧡 मराठी", use_container_width=True):
        st.session_state.language = "Marathi"
        st.rerun()
    if c3.button("🇮🇳 हिन्दी", use_container_width=True):
        st.session_state.language = "Hindi"
        st.rerun()
    st.stop()

# =========================================
# MAIN APP UI
# =========================================
st.title(f"🧩 Riddle Master ({st.session_state.language})")

with st.sidebar:
    st.header("⚙️ Settings")
    st.success("⚡ Offline Mode Active (Zero Lag)")
    st.divider()
    if st.button("🌐 Change Language", use_container_width=True):
        for key, value in defaults.items():
            st.session_state[key] = value
        st.rerun()

# SCOREBOARD
a, b, c = st.columns(3)
a.metric("🔥 Streak", st.session_state.streak)
b.metric("🏆 High Score", st.session_state.high_score)
c.metric("❤️ Lives", st.session_state.lives)
st.divider()

# =========================================
# GAMEPLAY LOOP
# =========================================
if st.session_state.current_riddle == "":
    load_new_riddle()
    st.rerun() # Instant reload without loading spinner!

if st.session_state.current_riddle:
    st.subheader("🧠 Your Riddle")
    st.info(st.session_state.current_riddle)

    # Hint Button
    if st.button("💡 Get Hint (-2 points)"):
        if st.session_state.streak >= 2:
            st.session_state.hint = st.session_state.hidden_hint
            st.session_state.streak -= 2
            st.rerun()
        else:
            st.warning("Need at least 2 points!")
            
    if st.session_state.hint:
        st.warning(f"💡 Hint: {st.session_state.hint}")

    # Status Messages
    if st.session_state.status_msg:
        if "Correct" in st.session_state.status_msg:
            st.success(st.session_state.status_msg)
        elif "Wrong" in st.session_state.status_msg:
            st.warning(st.session_state.status_msg)
        else:
            st.error(st.session_state.status_msg)

    # Input Form 
    if not st.session_state.show_next:
        with st.form("guess_form"):
            user_guess = st.text_input("Your Answer", placeholder="Type answer here...")
            submitted = st.form_submit_button("✅ Submit Answer", use_container_width=True)

            if submitted:
                correct_answer = st.session_state.real_answer.strip().lower()
                player_answer = user_guess.strip().lower()

                if player_answer == correct_answer:
                    st.session_state.status_msg = f"🎉 Correct! Answer was: {st.session_state.real_answer}"
                    st.session_state.streak += 10
                    if st.session_state.streak > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.streak
                    st.session_state.show_next = True
                else:
                    st.session_state.lives -= 1
                    if st.session_state.lives <= 0:
                        st.session_state.status_msg = f"💀 Game Over! Answer was: {st.session_state.real_answer}"
                        st.session_state.streak = 0
                        st.session_state.show_next = True
                    else:
                        st.session_state.status_msg = f"❌ Wrong! {st.session_state.lives} lives left."
                
                st.rerun()

    # Next Button
    if st.session_state.show_next:
        st.markdown("---")
        if st.button("➡️ GET NEXT RIDDLE", use_container_width=True, type="primary"):
            st.session_state.current_riddle = ""
            st.session_state.status_msg = ""
            st.session_state.show_next = False 
            st.rerun()
