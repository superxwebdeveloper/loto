let selected = [];

function toggle(x) {
    let current = document.getElementById("ball_" + x);
    if(selected.length < 5 && !selected.includes(x)) {
        selected.push(x);
        current.style.color = "white";
        current.style.backgroundColor = "dodgerblue";
    } else if(selected.includes(x)) {
        selected.pop(x);
        current.style.color = "dodgerblue";
        current.style.backgroundColor = "white";
    }
    document.getElementById("guess").value = selected;
}