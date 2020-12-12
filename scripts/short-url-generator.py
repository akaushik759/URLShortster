characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def combos(prefix,char_len,remaining):
    if remaining == 0:
        print(prefix)
        return
    
    for i in range(char_len):
        combos(prefix+char_arr[i],char_len,remaining-1)
    


combos('',len(characters),10)