{
    "components":[
        {
            "id":"c1",
            "label":"Component 1",
            "nodes":["n1", "n2", "n3", "n4", "n5", "n6", ],
            "node":{'width':12,
                    'height':13},
            "layout":{'logic':'grid',
                      'rows':2}
            },
        {
            "id":"c2",
            "label":"Component 2",
            "nodes":["n3"]
            },
        ],

    "nodes":{
        "n1":{"label":"Node 1"},
        "n2":{"label":"Node 2"},
        "n3":{"label":"Node 3"},
        "n4":{"label":"Node 2"},
        "n5":{"label":"Node 3"},
        "n6":{"label":"Node 2"},
        "n7":{"label":"Node 3"}
        },

    "links":[
        {"from":"n1",
         "to":"n2",
         "label":"Link 1"}
        ]
    }
