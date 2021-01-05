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
