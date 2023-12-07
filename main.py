import cv2
import pytesseract
import spacy
from os import listdir
from os.path import isfile, join
from spacy.lang.en import English
from spacy.matcher import PhraseMatcher

# Adjust to point to folder where receipts are stored
mypath = "C:\\Users\\hp\\Desktop\\downloaded_receipts"

def evaluate_from_images():
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    NER = spacy.load("en_core_web_trf")
    print("Found " + str(len(onlyfiles)) + " files")
    # print(onlyfiles)

    for filename in onlyfiles:
        image = cv2.imread(mypath + '\\' + filename)

        lines = pytesseract.image_to_string(image)

        lines = lines.split("\n")

        lines = filter(lambda line: line, lines)

        lines_list = list(lines)

        full_sentence = ""

        for line in lines_list:
            full_sentence += (" " + line)

        print(filename)
        print(full_sentence)
        text = full_sentence

        # nlp = English()
        # matcher = PhraseMatcher(nlp.vocab, attr="SHAPE")
        # matcher.add("DATETIME", [nlp("Fri Oct 06 15:38:59 WAT 2023"), nlp("Fri Oct 27 21:12:41 WAT 2023")])
        # matcher.add("DATETIME", [
        #     nlp("10-31 10:09:41"),
        #     nlp("03-23 10:39:41"),
        #     nlp("3-23 10:39:41"),
        #     nlp("2-3 10:39:41"),
        #     nlp("2023 2-3 10:39:41"),
        #     nlp("2023 12-13 20:59:45"),
        #     nlp("Oct 17, 2023 6:20:58"),
        #     nlp("Oct 17, 2023 06:20"),
        #     nlp("Oct 19,2023 06:20"),
        #     nlp("Oct 17, 2023 6:20"),
        #     nlp("Feb 20, 2023 7:40:58"),
        #     nlp("Oct 30,2023,16:06")
        # ])

        person_list = []
        date_list = []

        # for line in lines:
        doc = NER(text)
        for word in doc.ents:
            if (word.label_ == "DATE" or word.label_ == "TIME") and word.text.isnumeric() is False:
                date_list.append(word.text)
            if word.label_ == "PERSON":
                person_list.append(word.text)

        # doc = nlp(text)
        # matches = matcher(doc)
        # for match_id, start, end in matches:
        #     string_id = nlp.vocab.strings[match_id]  # Get string representation
        #     span = doc[start:end]  # The matched span
        #     print(match_id, string_id, start, end, span.text)


        print("Name: ")
        print(person_list)
        print("Dates")
        print(date_list)
        print()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    evaluate_from_images()
