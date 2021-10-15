def get_query(limit, offset):
    return f'''PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT DISTINCT ?a, ?dob, ?ht, ?name, ?c, ?intro
    WHERE{{?a a dbo:Athlete; dbo:birthDate ?dob; dbo:height ?ht;
    foaf:name ?name; dbo:abstract ?intro.
    OPTIONAL{{?a  dbo:country ?c}}
    FILTER(LANG(?name) = "en").
    }} LIMIT {limit} OFFSET {offset}'''