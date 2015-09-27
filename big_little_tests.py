#!/usr/bin/python
# -*- coding: utf-8 -*-

# 7 who want littles who have not had littles
# 6 who want littles who have not had littles
# 7 people want twins

big_rhianna = {
    'name': 'rhianna',
    'want': 2,
    'twins': 0,
    'pref': ['a', 'b', 'c'],
    'dying_family': 1,
    'has_little': 0,
    }

big_molly = {
    'name': 'molly',
    'want': 2,
    'twins': 0,
    'pref': ['tara', 'hara', 'jana'],
    'dying_family': 1,
    'has_little': 0,
    }

big_ariel = {
    'name': 'ariel',
    'want': 2,
    'twins': 0,
    'pref': ['lane', 'mara', 'zenon'],
    'dying_family': 1,
    'has_little': 0,
    }

big_snow = {
    'name': 'snow',
    'want': 1,
    'twins': 0,
    'pref': ['elsa', 'lane', 'kelly'],
    'dying_family': 1,
    'has_little': 0,
    }

big_belle = {
    'name': 'belle',
    'want': 1,
    'twins': 0,
    'pref': ['julia', 'betty', 'xena'],
    'dying_family': 0,
    'has_little': 0,
    }

big_carrie = {
    'name': 'carrie',
    'want': 1,
    'twins': 1,
    'pref': ['meg', 'pam', 'mara'],
    'dying_family': 1,
    'has_little': 0,
    }

big_miranda = {
    'name': 'miranda',
    'want': 1,
    'twins': 1,
    'pref': ['tara', 'hara', 'jana'],
    'dying_family': 0,
    'has_little': 0,
    }

big_samantha = {
    'name': 'samantha',
    'want': 1,
    'twins': 1,
    'pref': ['lane', 'mara', 'zenon'],
    'dying_family': 0,
    'has_little': 0,
    }

# 2+1-1 = 2

big_charlie = {
    'name': 'charlie',
    'want': 2,
    'twins': 1,
    'pref': ['julia', 'brenda', 'kelly'],
    'dying_family': 1,
    'has_little': 1,
    }

# 1+0-1 = 0

big_topanga = {
    'name': 'topanga',
    'want': 1,
    'twins': 1,
    'pref': ['julia', 'betty', 'xena'],
    'dying_family': 0,
    'has_little': 1,
    }

# 2+1-1 = 1

big_erica = {
    'name': 'erica',
    'want': 2,
    'twins': 1,
    'pref': ['meg', 'pam', 'barbie'],
    'dying_family': 0,
    'has_little': 1,
    }

# 1+0-1 = 0

big_jessica = {
    'name': 'jessica',
    'want': 1,
    'twins': 1,
    'pref': ['tara', 'hara', 'jana'],
    'dying_family': 0,
    'has_little': 1,
    }

# 1+0-2 = -1

big_nicole = {
    'name': 'nicole',
    'want': 1,
    'twins': 0,
    'pref': ['lana', 'mara', 'zenon'],
    'dying_family': 0,
    'has_little': 2,
    }

# 1+0-1 = 0

big_lily = {
    'name': 'lily',
    'want': 1,
    'twins': 0,
    'pref': ['meg', 'pam', 'barbie'],
    'dying_family': 0,
    'has_little': 1,
    }

big_robin = {
    'name': 'robin',
    'want': 0,
    'twins': 0,
    'pref': ['serena', 'riley', 'maya'],
    'dying_family': 1,
    'has_little': 0,
    }

big_tracy = {
    'name': 'tracy',
    'want': 0,
    'twins': 0,
    'pref': ['elsa', 'brenda', 'kelly'],
    'dying_family': 0,
    'has_little': 0,
    }

test_bigs1 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    big_charlie,
    big_topanga,
    big_erica,
    big_jessica,
    big_nicole,
    big_lily,
    big_robin,
    big_tracy,
    ]
test_result1 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    ]
test_result2 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    big_charlie,
    big_erica,
    big_topanga,
    ]
test_result3 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    big_charlie,
    big_erica,
    big_topanga,
    big_jessica,
    big_lily,
    big_nicole,
    ]
test_result4 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    big_charlie,
    big_topanga,
    big_erica,
    big_jessica,
    big_nicole,
    big_lily,
    ]
test_result5 = [
    big_rhianna,
    big_molly,
    big_ariel,
    big_snow,
    big_belle,
    big_carrie,
    big_miranda,
    big_samantha,
    big_charlie,
    big_topanga,
    big_erica,
    big_jessica,
    big_nicole,
    big_lily,
    big_robin,
    ]

little_tara = {'name': 'tara', 'pref': ['molly', 'ariel', 'snow']}
little_hara = {'name': 'hara', 'pref': ['belle', 'carrie', 'miranda']}
little_jana = {'name': 'jana', 'pref': ['samantha', 'charlie', 'topanga'
               ]}

little_lane = {'name': 'lane', 'pref': ['erica', 'jessica', 'nicole']}
little_mara = {'name': 'mara', 'pref': ['lily', 'robin', 'molly']}
little_zenon = {'name': 'zenon', 'pref': ['ariel', 'snow', 'carrie']}

little_elsa = {'name': 'elsa', 'pref': ['miranda', 'samantha', 'charlie'
               ]}
little_brenda = {'name': 'brenda', 'pref': ['topanga', 'erica',
                 'jessica']}
little_kelly = {'name': 'kelly', 'pref': ['nicole', 'lily', 'robin']}
little_julia = {'name': 'julia', 'pref': ['molly', 'ariel', 'snow']}

little_betty = {'name': 'betty', 'pref': ['belle', 'carrie', 'miranda']}
little_xena = {'name': 'xena', 'pref': ['samantha', 'charlie', 'topanga'
               ]}

little_meg = {'name': 'meg', 'pref': ['erica', 'jessica', 'nicole']}
little_pam = {'name': 'pam', 'pref': ['lily', 'robin', 'molly']}
little_barbie = {'name': 'barbie', 'pref': ['ariel', 'snow', 'belle']}

test_littles1 = [
    little_tara,
    little_hara,
    little_jana,
    little_lane,
    little_mara,
    little_zenon,
    little_elsa,
    ]

test_littles2 = [
    little_tara,
    little_hara,
    little_jana,
    little_lane,
    little_mara,
    little_zenon,
    little_elsa,
    little_brenda,
    little_kelly,
    little_julia,
    ]

test_littles3 = [
    little_tara,
    little_hara,
    little_jana,
    little_lane,
    little_mara,
    little_zenon,
    little_elsa,
    little_brenda,
    little_kelly,
    little_julia,
    little_betty,
    little_xena,
    little_meg,
    little_pam,
    little_barbie,
    ]

test_result6 = {
    'molly': 'tara',
    'ariel': 'zenon',
    'belle': 'hara',
    'miranda': 'elsa',
    'samantha': 'jana',
    'carrie': 'mara',
    'snow': 'lane',
    }
test_result7 = {
    'molly': 'tara',
    'ariel': 'zenon',
    'belle': 'hara',
    'miranda': 'elsa',
    'samantha': 'jana',
    'carrie': 'mara',
    'snow': 'julia',
    'erica': 'lane',
    'charlie': 'brenda',
    'rhianna': 'kelly',
    }

test_twins_bigs1 = [big_miranda, big_carrie]
test_twins_littles1 = [little_tara, little_meg, little_zenon]


big_nick = {
    'name': 'nick',
    'want': 2,
    'twins': 1,
    'pref': ['alex', 'kennon', 'tim'],
    'dying_family': 1,
    'has_little': 0,
    }

big_chris = {
    'name': 'chris',
    'want': 2,
    'twins': 1,
    'pref': ['kennon', 'tim', 'alex'],
    'dying_family': 0,
    'has_little': 0,
    }

big_josh = {
    'name': 'josh',
    'want': 1,
    'twins': 1,
    'pref': ['kat', 'kennon', 'tim'],
    'dying_family': 0,
    'has_little': 0,
    }

big_tony = {
    'name': 'tony',
    'want': 1,
    'twins': 1,
    'pref': ['kat', 'kennon', 'tim'],
    'dying_family': 0,
    'has_little': 0,
    }

little_alex = {'name': 'alex', 'pref': ['nick', 'chris', 'josh']}
little_kennon = {'name': 'kennon', 'pref': ['nick', 'chris', 'josh']}
little_tim = {'name': 'tim', 'pref': ['josh', 'chris', 'nick']}
little_kat = {'name': 'kat', 'pref': ['nick', 'chris', 'josh']}
little_miller = {'name': 'miller', 'pref': ['matt', 'eric', 'justin']}

bigs42 = [big_nick, big_chris, big_josh]
littles42 = [little_alex, little_kennon, little_tim, little_kat]
result42 = {'nick':'alex','nick_copy':'kennon','chris':'kat','josh':'tim'}

bigs52 = [big_nick, big_chris, big_josh, big_tony]
littles52 = [little_alex, little_kennon, little_tim, little_kat,little_miller]
result52 = {'nick':'alex','nick_copy':'kennon','chris':'kat','josh':'tim','tony':'miller'}





