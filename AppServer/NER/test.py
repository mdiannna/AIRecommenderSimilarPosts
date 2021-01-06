from rulebased import RuleBasedInformationExtractor


if __name__ == "__main__":
    extractor = RuleBasedInformationExtractor()
    # opt = extractor.extract_field_from_options("test a", "rase_caini.txt")
    
    sample_text1 = """S-a perdut in com.Tohatin, caine de rasa ,,BEAGLE,,, mascul pe nume ,,KAY,,
Va rugam frumos sa ne anuntati daca stiti ceva informatie despre prietenul familie, poate la-ti vazut prin priajma sau cineva la adapostit. Orice informatie este binevenita, oferim recompensa persoanelor care detin informatie veridica. 
Oameni buni, faceti bine azi pentru ca maine sa fiti fericiti pentru ceea ce ati facut ieri."""
    
    extracted_breeds = extractor.extract_breed("test a", verbose=True)
    print(extracted_breeds)

    extracted_breeds = extractor.extract_breed(sample_text1, verbose=True)
    print(extracted_breeds)

    extracted = extractor.extract_animal_type(sample_text1)
    print("Specie animal:", extracted)

    # For word tokenization:
    # from nltk.tokenize import word_tokenize
    # print(word_tokenize(sample_text1))


    print("---- extract from regex:---")
    sample_text2 = "Motan domestic pierdut! Dacă a fost găsit, rog să fiu contactat la tel.: 062167527. Garantez remunerare!. 123456789"

    extracted = extractor.extract_field_from_regex(sample_text2, regex_filename='telefon.txt', verbose=True)
    print(extracted)

    extracted = extractor.extract_phone(sample_text2, verbose=True)
    print(extracted)

    extracted = extractor.extract_animal_type(sample_text2)
    print("Specie animal:", extracted)


    print("---- test general extract_field() function---")
    extracted = extractor.extract_field(sample_text2, "specie", "options", "specie_animal.txt")
    print("Specie animal:", extracted)

    extracted = extractor.extract_field(sample_text2, "tel", "regex", "telefon.txt")
    print("Telefon:", extracted)

    print("---- sample text 3: ---")
    sample_text3 = """Buna ziua, ieri între orele 9:00-11:00 a ieșit din ograda ciinele Labrador Golden Retriever (Mailo) alb, virstă 7 luni, zgarda albastră, perimetru Șos. Muncești și Str. Burebista (Parcul de troleibuz)!
    După ultimele informatii era in raza Portilor Orasului!
    Tel. 069063867
    Ofer Recompensă!!!!"""

    extracted = extractor.extract_field(sample_text3, "specie", "options", "specie_animal.txt", verbose=False)
    extracted_phone = extractor.extract_field(sample_text3, "tel", "regex", "telefon.txt", verbose=False)
    extracted_breeds = extractor.extract_breed(sample_text3, verbose=False)


    print("Specie animal:", extracted)
    print("Telefon:", extracted_phone)
    print("Rasa:", extracted_breeds)


    extracted_reward = extractor.extract_field(sample_text3, "recompensa", "options", "recompensa.txt", verbose=False)
    print("Recompensă: (cu optiuni nu prea merge, trebuie NER NN):", extracted_reward)






    