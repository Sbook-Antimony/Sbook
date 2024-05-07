
var hoverCls = document.querySelectorAll("[hover-class=*]");
document.querySelectorAll("[hover-class=*]").forEach((element) => {
    element.addEventListener("hover", function() {
        element.classList.add(
            ...element.getAttribute("hover-class").split(" ")
        );
    });
});

var viewCls = document.querySelectorAll("[view-class=*]");
document.querySelectorAll("[view-class=*]").forEach((element) => {
    element.addEventListener("mouseenter", function() {
        element.classList.add(
            ...element.getAttribute("view-class").split(" ")
        );
    });
    element.addEventListener("mouseleave", function() {
        element.classList.remove(
            ...element.getAttribute("view-class").split(" ")
        );
    });
});
