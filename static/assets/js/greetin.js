// let greet_element = document.querySelector(".greeting").innerHTML

const date = new Date();
const time = date.getHours();

if(time < 12 ){
    document.querySelector('.greeting').innerHTML = "Good Morning"
}else if(time >= 12 && time < 17 ){
    document.querySelector('.greeting').innerHTML = "Good Afternoon"
}
else {
    document.querySelector('.greeting').innerHTML = "Good Evening"
}

console.log(time)