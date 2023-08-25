window.onload = async function() {
    text = document.createElement("span");
    document.body.appendChild(text);
    
    text.style.font = "\"Muli\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\", \"Noto Color Emoji\"";
    text.style.fontSize = "20px";
    text.style.height = 'auto';
    text.style.width = 'auto';
    text.style.position = 'absolute';
    text.style.whiteSpace = 'no-wrap';
    text.innerHTML = document.querySelector('.item.last div').innerHTML;
    
    width = Math.ceil(text.clientWidth);
    formattedWidth = width + "px";
    
    document.querySelector('.item.last div').setAttribute("style", "--width: "+formattedWidth+";");
    document.body.removeChild(text);
}