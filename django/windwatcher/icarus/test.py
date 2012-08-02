#!/usr/bin/python

#Acts as a constant time lookup for if a condition is good or not
wind_conditions_good = {
    'no lift':False,
    'poor':False,
    'fair':True,
    'good':True,
    'dangerous wind':False
}

#Converts various combinations of site possibilities into total site flyability
#TODO: make this less hackey/proper
site_conditions = { 'good': {},'fair': {} }
site_conditions['good']={'good':'Excellent','fair':'Good'}
site_conditions['fair']={'good':'Good','fair':'Fair'}

"""Checks weather conditions for all landings associated with a site
Takes a site object
returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
def _landing_check():
    print "Landing check stub" 
    return {54:'good',63:'good'}

"""Checks weather conditions for all launches associated with a site
Takes a site object
returns a dict of flyable launches with format [launch_id]:['no lift'|'poor'|'fair'|'good'|'dangerous wind']"""
def _launch_check():
    print "Launch check stub" 
    return {323:'dangerous wind',32:'fair',43:'poor'}

"""Checks if there are at least 1 fair|good launch and 1 'fair'|'good' landing
Takes a site object
returns fair if the best case is two are fair, good if one is good, and excellent if both are good"""
def site_check():
    print "Site check stub" 
    #return list of known words for site conditions, this function is naive about which launch/landing it is, don't care
    #TODO: add in object passing down to private functions
    launchability =  [ flyability for site_id,flyability in _launch_check().iteritems() if wind_conditions_good[flyability] ]
    landability =  [ flyability for site_id,flyability in _landing_check().iteritems() if wind_conditions_good[flyability] ]
    #condense list to best case
    for launch_condition in launchability:
        #if we find good that's it, we're done looking
        if launch_condition == 'good':
            break #else we have fair
    for landing_condition in launchability:
        if landing_condition == 'good':
            break 
    #Lookup overall resultant flyability of site based on launch/landing combos
    print site_conditions[launch_condition][landing_condition] 
if __name__ == "__main__":
    site_check()


