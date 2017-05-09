import pandas as pd
import re

df = pd.read_csv('test_borrar.csv')

grouped_df =df.sort_values('Comment_n',ascending=True).groupby('Thread_URL')

for t in grouped_df['Thread_URL']:
    _, k = t
    if len(k.index) > 1:
      #print(len(k.index), k.index)
      prev_user=""
      total_message = []
      old_total_message = []
      old_prev_user=""
      for i in k.index:
        message = str(df['Comment_Text'][i]).strip()
        user = df ['UserID'][i]
        #print(user,": ", message)
        if user != prev_user and ("movistar" in user.lower() or "movistar" in prev_user.lower()):
          if len(total_message) > 0:
            #clean up a bit, quitar @usuario escribió:
            for i in range(len(total_message)):
              if " escribió:" in total_message[i]:
                for old_message in old_total_message:
                  total_message[i] = total_message[i].replace(old_message,"")
                  #total_message[i] = re.sub('^.*escribió:','LOHEQUITADO, había esto: ###' + old_message + '###', total_message[i])
                  total_message[i] = re.sub('^.*escribió:','', total_message[i])
              if old_prev_user != "":
                total_message[i] = total_message[i].replace('Hola ' + old_prev_user,'Hola NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Hola otra vez ' + old_prev_user,'Hola otra vez NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos días ' + old_prev_user,'Buenos días NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos tardes ' + old_prev_user,'Buenos tardes NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos noches ' + old_prev_user,'Buenos noches NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Hola @' + old_prev_user,'Hola NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Hola otra vez @' + old_prev_user,'Hola otra vez NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos días @' + old_prev_user,'Buenos días NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos tardes @' + old_prev_user,'Buenos tardes NOMBRE_DE_USUARIO ')
                total_message[i] = total_message[i].replace('Buenos noches @' + old_prev_user,'Buenos noches NOMBRE_DE_USUARIO ')

            
            if "movistar" in prev_user.lower():
              print(prev_user + ":", (" SEPARADOR_DE_FRASES ".join(total_message)).strip())
            else:
              print(prev_user+":", (" ".join(total_message)).strip())
            old_total_message = total_message
            old_prev_user = prev_user
          total_message =[]
          
        total_message.append(message)  
        
        prev_user = user
        
      if "movistar" in prev_user.lower():
        print(prev_user,": ", " SEPARADOR_DE_FRASES ".join(total_message))
      else:
        print(prev_user,": ", " ".join(total_message))
      print("===")
    
