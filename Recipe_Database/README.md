# Recipe_Database

This service is a database hosted on a web server to store recipe and ingredients.

## Data Request

To request data from the service, send an HTTP GET request to /recipes and await the response. You may use url optional queries on name and limit to adjust the query for recipe
The response from the server will be sent in JSON format. An example request and response is shown below.

An example request in javascript:
```javascript
fetch('http://localhost:5000/recipes?name=rice&limit=5')
.then(response => response.json())
.then(response => () =>{//do something with the data})
```

An example response:
```json
{
    "9": {
        "calories": 375,
        "ingredients": [
            {
                "name": "Rice",
                "quantity": 1.0,
                "units": "cup"
            },
            {
                "name": "Corn",
                "quantity": 0.25,
                "units": "cup"
            },
            {
                "name": "Peas",
                "quantity": 0.25,
                "units": "cup"
            },
            {
                "name": "Sausage",
                "quantity": 0.5,
                "units": "cup"
            },
            {
                "name": "Egg",
                "quantity": 1.0,
                "units": ""
            },
            {
                "name": "Soy Sauce",
                "quantity": 3.0,
                "units": "teaspoon"
            }
        ],
        "name": "Fried Rice"
    }
}
```

## Data Send

To send data to the service, send an HTTP Post request to /recipes with body formatted as a JSON string. An example is below:
```javascript
let body = {
    "name":"Green Onion Fried Tofu",
    "calories": 325,
    "ingredients":[
        {"name":"Green Onion", "quantity":1, "units":""},
        {"name":"Tofu", "quantity":1, "units":"teaspoon"},
        {"name":"Olive Oil", "quantity":0.25, "units":"cup"},
        {"name":"Salt", "quantity":1, "units":"pinch"}
    ]
}

fetch('http://localhost:5000/recipes', {
  method: "POST",
  body: JSON.stringify(body),
  headers: {
      'Content-Type': 'application/json'
    }
})
```

## UML

![UML](https://github.com/cnguyen0320/Recipe_Database/blob/main/UML.png)
