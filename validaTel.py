def telValidation(tel):
    regex = r"^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$"
    result = ''
    test_str = tel
    matches = re.finditer(regex, test_str, re.MULTILINE)

    if tel == '':
        return {"message":"Digite seu telefone!"}
    
    
    for matchNum, match in enumerate(matches, start=1):
        
        result = "Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group())
    
   
    if result == '':
        return {"message":"Telefone inválido!"}
    else:
        return {"message":""}   
