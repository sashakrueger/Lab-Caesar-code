from collections import Counter
import re
alphabet = "а,б,в,г,д,е,ё,ж,з,и,й,к,л,м,н,о,п,р,с,т,у,ф,х,ц,ч,ш,щ,ъ,ы,ь,э,ю,я"
alphabet = alphabet.split(",")
ceazar_alphabet = alphabet.copy()
new_alphabet = list('оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфъё')
key = ""
keyword = ""


def test():
    global key
    global keyword
    key = input("Введите сдвиг (число в промежутке 1-32): ")
    if not key.isdigit():
        return 0
    key = int(key)
    if key >= len(alphabet) or key < 1:
        return 0
    keyword = input("Введите ключевое слово: ")
    keyword = list(keyword)
    for i in keyword:
        if i not in alphabet:
            return 0
    if len(keyword) != len(set(keyword)):
        return 0
    if len(keyword) >= len(alphabet):
        return 0
    return 1


while True:
    if test():
        break


def ceazar_crypt(encrypt, keyword, key):
    encrypt = encrypt.lower()
    encrypted = []
    for i in keyword:
        ceazar_alphabet.pop(ceazar_alphabet.index(i))  # удаление всех букв ключ-слова из алфавита
    keyword.reverse()
    for j in keyword:
        ceazar_alphabet.insert(0, j)  # вставка в начало
    for о in range(key):
        ceazar_alphabet.insert(0, ceazar_alphabet.pop())  # сдвиг

    for letter in encrypt:
        if letter in ceazar_alphabet:
            encrypted.append(ceazar_alphabet[alphabet.index(letter)])
        else:
            encrypted.append(letter)
    encrypted = "".join(encrypted)
    print("Русский алфавит:\t", alphabet, "\nАлфавит Цезаря:\t\t", ceazar_alphabet)
    return encrypted


# чтение
WarAndPeace = open("WarAndPeaceFull3.txt", "rt")
textWP = WarAndPeace.read().lower()
# запись в файл зашифрованной версии
with open("CaesarWarAndPeace_Encrypted.txt", "w") as CaesarWarAndPeace_Encrypted:
    CaesarWarAndPeace_Encrypted.write(ceazar_crypt(textWP, keyword, key))


# расшифровка(монограммы)
CaesarWarAndPeace_Encrypted = open("CaesarWarAndPeace_Encrypted.txt", "rt")
textEncrypted = CaesarWarAndPeace_Encrypted.read()
frequency = Counter("".join([ch for ch in textEncrypted if ch in alphabet]))
print(f"Частота встречи букв в шифре цезаря:\t{len(frequency)} {frequency}")
temp_list = list(frequency.items())
temp_list.sort(key=lambda i: i[1])
temp_list.reverse()
frequency = []
for i in temp_list:
    frequency.append(i[0])
#  frequency массив с буквами которые чаще всего встречаются в тексте цезаря
while len(frequency) != len(alphabet):
    frequency.append('')
# расшифровка
textDecrypted = []
for i in textEncrypted:
    if i in alphabet:
        textDecrypted.append(new_alphabet[frequency.index(i)])
    else:
        textDecrypted.append(i)
textDecrypted = "".join(textDecrypted)

# запись в файл
with open("CaesarWarAndPeace_Decrypted_v1.txt", "w") as CaesarWarAndPeace_Decrypted:
    CaesarWarAndPeace_Decrypted.write(textDecrypted)

# биграммы
beGramsOg = Counter(re.findall(r'(?=([а-я]{2}))', textWP)).most_common(10)
bigrams = []
for i in beGramsOg:
    bigrams.append(i[0])
print(f"Популярные биграммы в оригинальном тексте:\t\t{bigrams}")
beGrams = Counter(re.findall(r'(?=([а-я]{2}))', textDecrypted)).most_common(10)
DecryptedBeGrams = []
for i in beGrams:
    DecryptedBeGrams.append(i[0])
print(f"Популярные биграммы в расшифрованном тексте:\t{DecryptedBeGrams}")
print(f"Алфавит для расшифровки(монограммы):\t{new_alphabet}")

ListOfBigrams_new = []
ListOfBigrams = []
for i in range(len(DecryptedBeGrams)):

    if DecryptedBeGrams[i] != bigrams[i]:
        DecryptedBeGramsItem = list(DecryptedBeGrams[i])
        OgBeGramsItem = list(bigrams[i])
        
        for i in range(len(DecryptedBeGramsItem)):
            if DecryptedBeGramsItem[i] != OgBeGramsItem[i]:
                if DecryptedBeGramsItem[i] not in ListOfBigrams_new and DecryptedBeGramsItem[i] not in ListOfBigrams:
                    ListOfBigrams_new.append(DecryptedBeGramsItem[i])

                if OgBeGramsItem[i] not in ListOfBigrams_new and OgBeGramsItem[i] not in ListOfBigrams:
                    ListOfBigrams.append(OgBeGramsItem[i])

for i in range(len(ListOfBigrams_new)):

    new_alphabet[new_alphabet.index(ListOfBigrams_new[i])], new_alphabet[new_alphabet.index(ListOfBigrams[i])] = "GG", ListOfBigrams_new[i]
    new_alphabet[new_alphabet.index("GG")] = ListOfBigrams[i]
print(f"Алфавит для расшифровки(монограммы и биграммы):\t{new_alphabet}")

# Расшифровка с новым алфавитом
textDecrypted2 = []
for i in textEncrypted:
    if i in alphabet:
        textDecrypted2.append(new_alphabet[frequency.index(i)])
    else:
        textDecrypted2.append(i)
textDecrypted2 = "".join(textDecrypted2)
# запись
with open("CaesarWarAndPeace_Decrypted_v2.txt", "w") as CaesarWarAndPeace_Decrypted2:
    CaesarWarAndPeace_Decrypted2.write(textDecrypted2)
CaesarWarAndPeace_Encrypted.close()
WarAndPeace.close()
