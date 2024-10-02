const field = document.querySelector(".artist-names-area")
const eventSource = new EventSource("/update-artists")
eventSource.onmessage = (e) => {
    console.log("hit")
    field.innerText = e.data
}
