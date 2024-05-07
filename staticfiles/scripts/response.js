
var hoverCls = document.querySelectorAll("[hover-class=*]");
document.querySelectorAll("[hover-class=*]").forEach((element) => {
    element.addEventListener("mouseenter", function() {
        element.classList.add(
            ...element.getAttribute("hover-class").split(" ")
        );
    });
    element.addEventListener("mouseleave", function() {
        element.classList.remove(
            ...element.getAttribute("hover-class").split(" ")
        );
    });
});

var viewCls = document.querySelectorAll("[view-class=*]");
document.querySelectorAll("[view-class=*]").forEach((element) => {
      
    let observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            // Each entry describes an intersection change for one observed
            // target element:
            //   entry.boundingClientRect
            //   entry.intersectionRatio
            //   entry.intersectionRect
            //   entry.isIntersecting
            //   entry.rootBounds
            //   entry.target
            //   entry.time
            if(entry.isIntersecting) {
                element.classList.add(
                    ...element.getAttribute("hover-class").split(" ")
                );
            } else {
                element.classList.remove(
                    ...element.getAttribute("hover-class").split(" ")
                );
            }
        },
    {
        root: null,
        rootMargin: "0px",
        threshold: 1.0,
    });
    observer.observe(element);
});
