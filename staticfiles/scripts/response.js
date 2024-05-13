
document.querySelectorAll("[hover-class]").forEach((element) => {
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

document.querySelectorAll("[view-class]").forEach((element) => {
    new IntersectionObserver(
        (entries, observer) => {
            console.log("viez", entries, observer);
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
            });
        },
        {
            root: null,
            rootMargin: "0px",
            threshold: [1.0, 0.5, 0.0],
        },
    ).observe(element);
});