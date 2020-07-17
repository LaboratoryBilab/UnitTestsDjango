let data

const xhr = new XMLHttpRequest()
xhr.open('GET', '/static/crop1_rus_parsed.json', false)
//xhr.open('GET', '/static/crop.json', false)

xhr.send()
data = JSON.parse(xhr.responseText)

function request(url) {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '/' + url + '/', true)
    //xhr.setRequestHeader("ForecastMethod", "RF");
    xhr.setRequestHeader("ForecastMethod", "RF");
    //xhr.setRequestHeader("ForecastMethod", "RF");

    xhr.onreadystatechange = () => {
        if (xhr.readyState != 4) return
        console.log(JSON.parse(xhr.responseText))
    }
    xhr.send(JSON.stringify(data))
}
