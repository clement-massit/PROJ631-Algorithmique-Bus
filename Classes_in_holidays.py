# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


import manip_data

#==============================================================================  
#CLASSE ARRET    
class Arret:
    """
    A stop possesses a label -> the name of the stop
    """
    def __init__(self,label):
        self.label = label
        
    def get_label(self):  #retourne le nom d'un arret
        return self.label 
        
    def get_ligne(self):
        '''
        get the line of a stop
        if the stop belong to many lines, the line refers to the line of start
        '''
        ligne = ''
        dico_l1 = manip_data.holidays_horaires(ligne1.get_name_ligne())
        dico_l2 = manip_data.holidays_horaires(ligne2.get_name_ligne())
        
        for key in dico_l1.keys():
            if self.get_label() not in dico_l2:
                ligne = ligne1.get_name_ligne()
                break
            if self.get_label() not in dico_l1: 
                ligne = ligne2.get_name_ligne()
                break
            else:   
                if start.get_label() == key:
                    ligne = ligne1.get_name_ligne()
                    break
                else:
                    ligne = ligne2.get_name_ligne()
                
        return ligne   

    def next_depart(self,time_start):
        '''
        return the next timetable of the next stop
        from the first path (this is for the shortest way)
        '''
        
        liste_horaire = self.horaires_first_path()
       
        time = manip_horaire(time_start)
        
        if time == True:
            ntime = liste_horaire.index(time + 1)
            for m in liste_horaire:
                horaire_compare = manip_horaire(m)
                if horaire_compare > ntime:
                    break
        else:
            for m in liste_horaire:
                horaire_compare = manip_horaire(m)
                if horaire_compare > time:
                    break
                
        return convert_to_hours_minutes(horaire_compare)
    
    
    def next_depart_sec_path(self,time_start):
        '''
        return the next timetable of the next stop
        from the second path (this is for the shortest way)
        '''
        
        liste_horaire = self.horaires_sec_path()
       
        time = manip_horaire(time_start)
        
        if time == True:
            ntime = liste_horaire.index(time + 1)
            for m in liste_horaire:
                horaire_compare = manip_horaire(m)
                if horaire_compare > ntime:
                    break
        else:
            for m in liste_horaire:
                horaire_compare = manip_horaire(m)
                if horaire_compare > time:
                    break
        return convert_to_hours_minutes(horaire_compare)
    
    
    
    def horaires_first_path(self):
        '''
        with this method, we can get the list of timetable from one stop
        if there are one stop in two ligns, the we can get the correct line
        with the get_ligne() method
        '''
        dico = manip_data.holidays_horaires(self.get_ligne())  
        horaires = dico[self.get_label()]
        
        return horaires
    
    
    def get_index_horaire_du_next_arret(self,time):  
        '''
        return the index of timetable (indicated in parameters) of the new stop in the path
        this one is for the first_path() method (shortest way))
        '''
        liste_horaires_ar = self.horaires_first_path()
        
        horaire_next_depart = self.next_depart(time)  
       
        #heure du prochain bus a l'arret ar
        index_depart = liste_horaires_ar.index(horaire_next_depart)
    
        for h in range(len(liste_horaires_ar)):
        
            if index_depart == liste_horaires_ar[h]:
                break
        return index_depart
    
    def get_index_horaire_du_next_arret_sec_path(self,time):
        '''
        same than before but this one is for the second path (shortest way)
        '''
        liste_horaires_ar = self.horaires_sec_path()
        
        horaire_next_depart = self.next_depart_sec_path(time) 

        #heure du prochain bus a l'arret ar
        index_depart = liste_horaires_ar.index(horaire_next_depart)
    
        for h in range(len(liste_horaires_ar)):
        
            if index_depart == liste_horaires_ar[h]:
                break
        return index_depart


def build_stop(ar): #you can build a stop with this method
    return Arret(ar)


#==============================================================================
#CLASSE LIGNE       

class Ligne:
    '''
    a line possesses a label same as the Stop class
    '''
    def __init__(self, name_ligne):
        self.name_ligne = name_ligne #returns str
    
    def get_name_ligne(self):
        return self.name_ligne  #returns str    
    
    def existe_dans_ligne(self,arret):
        for arr in manip_data.get_path_regular(self.get_name_ligne()):
            
            if arret == arr:
                return True
        
ligne1 = Ligne('1_Poisy-ParcDesGlaisins.txt')
ligne2 = Ligne('2_Piscine-Patinoire_Campus.txt')

#==============================================================================
#HORAIRES

from datetime import timedelta
  

def manip_horaire(time):
    #this method can convert a timetable like HH:MM into a number of minutes
    h = time
    if h != '-':
        delta = timedelta(hours = int(h.split(':')[0]), minutes = int(h.split(':')[1]))
        minutes = delta.total_seconds()/60
        return minutes
    else:
        return True

def convert_to_hours_minutes(number):
    '''
    This is the reverse of the previous method
    convert a number of minutes into HH:MM
    '''
    hours = number // 60
    number -= (hours * 60)
    minutes = number 
    return '{:1}:{:02}'.format(int(hours), int(minutes))


def get_last_time(liste,timestart):
    #Give the last timetable of stop list from a start timetable
    for ar in liste:
        
        index_useful = Arret(ar).get_index_horaire_du_next_arret(timestart)
        heure_first = Arret(ar).horaires_first_path()[index_useful]
        timestart = heure_first
    time_done = timestart
    
    return time_done

def get_temps_du_trajet(liste,start,end):  
    #return the time spent in the bus during the travel
    time_debut = start.next_depart(timestart)
    time_fin= get_last_time(liste,timestart)
  
    
    minutes_debut = manip_horaire(time_debut)
    minutes_fin = manip_horaire(time_fin)
    
    time_trajet = minutes_fin - minutes_debut
    
    
    return round(time_trajet)

# =============================================================================
#   FASTEST WAY
    
def trajet_sur_une_ligne(start,end):
    #only one line, if the start stop is on the same line than the final stop
    dico = manip_data.holidays_horaires(start.get_ligne())
    chemin = []
    
    for key in dico.keys():
        chemin.append(key)
         
        if key == end.get_label():
            break
        
    del chemin[0:chemin.index(start.get_label())]     
    return chemin
    
def trajets_switchs(start,end):
    '''
    allow the bus switches, two stop possible to switch, GARE and VIGNIÈRES
    so it gives two possible paths
    this method returns a path or 2 paths
    '''
    
    dico = manip_data.holidays_horaires(start.get_ligne())
    path = []
    for key in dico.keys():
        path.append(key)
        
    if start.get_ligne() == end.get_ligne(): 
        chemin = trajet_sur_une_ligne(start,end)     
        return chemin
    else:
        
        switch = 'GARE'
        trajet_switched = re_switch(switch,end)
        trajet = path[path.index(start.get_label()):path.index(switch)+1]
        final = trajet + trajet_switched
        
    
        switch = 'VIGNIÈRES'
        total = []
        trajet_switched = re_switch(switch,end)
        trajet = path[path.index(start.get_label()):path.index(switch)+1]
        total = trajet + trajet_switched
        
        return final,total
 

   
def re_switch(switch,end):
    '''
    one switch during the travel
    it returns only the final steps after switching
    '''
    trajet = trajet_sur_une_ligne(start,end)
    if trajet[-1] != end.get_label():
        path = []
        dico = manip_data.holidays_horaires(end.get_ligne())
        for key in dico.keys():
            path.append(key)
            
        if switch == 'GARE':

            del path[0:trajet.index(switch)+1]
        else:
            
            del path[0:path.index(switch)]
        return path
    


def possible_times(start,end):
    '''
    calculating possible times of travels
    it returns times in number of minutes
    '''
    if start.get_ligne() != end.get_ligne():
            
        trajets = trajets_switchs(start,end)
       
        other = first_path() + sec_path()
        
        time1 = get_temps_du_trajet(trajets[0],start,end)
        time2 = get_temps_du_trajet(trajets[1],start,end)
        time3 = get_temps_du_trajet(other,start,end)
        
        return time1,time2,time3
    else:
        trajet = trajet_sur_une_ligne(start,end)
        other = first_path() + sec_path()
        
        time1 = get_temps_du_trajet(trajet,start,end)
        time2 = get_temps_du_trajet(other,start,end)
        
        return time1,time2

def get_trajet_rapide(time,start,end):
    '''
    return the travel associated with a number of minutes
    //link with the preivous method
    it returns a path and only one path
    '''
    if start.get_ligne() == end.get_ligne():
        if time == possible_times(start,end)[0]: 
            return trajets_switchs(start,end)
        else:
            return first_path() + sec_path()
    else:
        if time == possible_times(start,end)[0]:
            return trajets_switchs(start,end)[0]
        if time == possible_times(start,end)[1]:
            return trajets_switchs(start,end)[1]
        else:
            return first_path() + sec_path()



def best_time(start,end):
    '''
    now we have all the paths we can calculate the time and return the best time
    concerning the time travel
    This method returns the smallest time of travelling 
    //link with previous methods in order to implement the fastest way method
    '''
    if start.get_ligne() == end.get_ligne():
        time1 = possible_times(start,end)[0]
        time2 = possible_times(start,end)[1]
        return min(time1,time2)
    else:
        time1 = possible_times(start,end)[0]
        time2 = possible_times(start,end)[1]
        time3 = possible_times(start,end)[2]
        return min(time1,time2,time3)



#==============================================================================
#   SHORTEST WAY
def first_path():
    #in order to switch line     
    dico = manip_data.holidays_horaires(start.get_ligne())
    
    chemin = []
    
    
    for cle in dico.keys():
        chemin.append(cle)
        
    del chemin[0:chemin.index(start.get_label())]
  
    for ar in chemin:  
        if ar == end.get_label():
            del chemin[chemin.index(ar)+1:]
            return chemin 
         
        if ligne1.existe_dans_ligne(ar) == True and ligne2.existe_dans_ligne(ar) == True: 
            del chemin[chemin.index(ar)+1:]        
            return chemin 

#switching line
def sec_path():  
    if first_path()[-1] == end.get_label():
        
        return []
 
    #1st switch 
    ligne_at_start = start.get_ligne()
   
    if ligne_at_start == ligne1.get_name_ligne():
        switch = ligne2.get_name_ligne()
    else:
        switch = ligne1.get_name_ligne()
        
   
    dico = manip_data.holidays_horaires(switch)
    chemin = []
    for cle in dico.keys():
        chemin.append(cle)
    liste_arret = first_path()
    
    index = chemin.index(liste_arret[-1])
    
    del chemin[0:index+1]
    
    for ar in chemin:
        if ligne1.existe_dans_ligne(ar) == True and ligne2.existe_dans_ligne(ar) == True:
            del chemin[chemin.index(ar)+1:]
    if end.get_label() == chemin[-1]:
        
        return chemin
    
   
    ##reswitch 
    if end.get_label() != chemin[-1]:
        if end.get_ligne() == Arret(chemin[-1]).get_ligne():
            ligne_at_start = ligne_at_start
            
        else:
            ligne_at_start = switch            
        new_dico = manip_data.holidays_horaires(ligne_at_start)
        new_list = []
        
        for key in new_dico.keys():
            new_list.append(key)
     
        new_index = new_list.index(first_path()[-1])
        fin_index = new_list.index(end.get_label()) 
       
        for ar in new_list:
        
            if ar == chemin[-1]:
                new_list = new_list[new_index:fin_index+1]
          
        return new_list


def possible_paths(sart,end):
    '''
    like fastes way method, we can enumerate some paths
    it returns a list of paths
    '''
    if start.get_ligne() == end.get_ligne():
        trajet = trajet_sur_une_ligne(start,end)
        other =  other = first_path() + sec_path()
        
        return trajet, other
    else:
        trajets = trajets_switchs(start,end)
        other = first_path() + sec_path()
        
        return trajets[0],trajets[1],other
    
    
    
def best_trajet(start,end):
    '''
    now we want the best travel concerning the number of stop
    this method returns the shortest way it terms of lenght of list
    '''
    
    if start.get_ligne() == end.get_ligne():
        paths = possible_paths(start,end)
        return paths[0] if len(paths[0]) < len(paths[1]) else paths[1] 
    else:
        paths = possible_paths(start,end)
        if len(paths[0]) < len(paths[1]) and len(paths[0]) < len(paths[2]):
            return paths[0]
        if len(paths[1]) < len(paths[0]) and len(paths[1]) < len(paths[2]):
            return paths[1]
        else:
            return paths[2]


#==============================================================================   
# FOREMOST WAY
def foremost(start,end):
    '''
    the foremost path implements the way that arrive the earliest.
    It takes some previous methods in order to list the paths.
    '''
    if start.get_ligne() == end.get_ligne():
        trajet = possible_paths(start,end)
        
        first, sec = trajet[0], trajet[1]
        time_first = manip_horaire(get_last_time(first,timestart))
        time_sec = manip_horaire(get_last_time(sec,timestart))
        mini = min(time_first, time_sec)
        if mini == time_first:
            return first, time_first
        else:
            return sec, time_sec
    else:
        
        trajet = possible_paths(start,end)
        one,two,three = trajet[0], trajet[1], trajet[2]
        time_one = manip_horaire(get_last_time(one,timestart))
        time_two = manip_horaire(get_last_time(two,timestart))
        time_three = manip_horaire(get_last_time(three,timestart))
        mini = min(time_one, time_two, time_three)
        
        if mini == time_one:
            return one, time_one
        if mini == time_two:
            return two, time_two
        else:
            return three, time_three   
        
#==============================================================================            
#CONSTRUCTION

def build_test(start,end,timestart):
    print(' ***  holiday timetables *** ') 
    plus_court = best_trajet(start,end)
    print('\n chemin le plus court :\n')
    for i in plus_court:
        print('\t-',i)
    print()    
    time_trajet_court = get_temps_du_trajet(plus_court,start,end)
    print('time travel :', time_trajet_court, 'minutes')
      
    
    print('\n------------------\n')
    plus_rapide = get_trajet_rapide(best_time(start,end), start,end)
    print('chemin le plus rapide :\n')
    for i in plus_rapide:
        print('\t-',i)
    print()    
    time_trajet_rapide = get_temps_du_trajet(plus_rapide,start,end)
    print('time travel :', time_trajet_rapide, 'minutes') 
    print('\n------------------\n')
    
    
    plus_tot = foremost(start,end)[0]
    print('chemin arrivant le plus tot :\n')
    for i in plus_tot:
        print('\t-', i)
    print()
    time_trajet_tot = get_temps_du_trajet(plus_tot,start,end)
    print('time travel :', time_trajet_tot, 'minutes\n') 
    return 'done'


def main():
    global start, end, timestart,realtime
    print('\n\t ENTER A START STOP :')
    start = build_stop(input())
    print('\t ENTER A FINAL STOP :')
    end = build_stop(input())
    print('\t ENTER A START TIMETABLE :')
    timestart = input()
    '''start = build_stop('Parc_des_Sports')
    end = build_stop('VIGNIÈRES')
    timestart = '6:00' '''
    realtime = timestart
    
    print(build_test(start,end,timestart))
    
    
if __name__ == "__main__":
    main()
