{
    "components":[
        {
            "id":"root",
            "label":"Component 1",
            "children":["n1", "n2", "n3", "n4", "n5", "n6", "c2", "c10", "n11"],
            "node":{'width':12,
                    'height':13},
            "layout":{'logic':'grid' 
                      }
            },
        {
            "id":"c2",
            "label":"Component 2",
            "children":["n7"]
            },
        {"id":"n1", "label":"Node 1", "width":100},
        {"id":"n2", "label":"Node 2"},
        {"id":"n3", "label":"Node 3"},
        {"id":"n4", "label":"Node 4"},
        {"id":"n5", "label":"Node 5"},
        {"id":"n6", "label":"Node 6"},
        {"id":"n7", "label":"Node 7", "children":["n8", "n9", "n10"], "layout":{"logic":"grid",
                                                                                "columns":1}},
        {"id":"n8", "label":"Node 6"},
        {"id":"n9", "label":"Node 6", "stroke":"#FFFF00"},
        {"id":"n10", "label":"Node 6"},
        {"id":"n11", "label":"Node 6"},
        {"id":"c10", "label":"floating ...",
         "children":["c3", "c4"]},
        {"id":"c3",
         "children":["c5"]},
        {"id":"c4",
         "children":["c5"]},
        {"id":"c5", "stroke":"#00FF00"},

        ],

    "links":[
        {"from":"n1",
         "to":"n2",
         "label":"Link 1"}
        ]
    }
