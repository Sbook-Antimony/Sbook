
for(let element of  $("[hover-class]")) {
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
};

for(let element of  $("[css-transition]")) {
    element.style.transition = element.getAttribute("css-transition");
};

for(let element of $("[view-class]")) {
    let margin = "10";
    (new IntersectionObserver(
        (entries, observer) => {
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
                let cls = element.getAttribute("view-class");

                if(!cls) return;


                cls = cls.split(" ");
                if(cls[0].endsWith(":")) {
                    [margin, ...cls] = cls;
                    margin = margin.slice(0,-1);
                }
                let ncls = cls.filter((c) => c.startsWith("!"));
                cls = cls.filter((c) => !c.startsWith("!"));
                for(var i = 0; i < ncls.length; i++) ncls[i] = ncls[i].slice(1);
                
                                
                try {
                    if(entry.isIntersecting) {
                        //console.log("added", ...element.getAttribute("view-class").split(" "));
                        element.classList.add(
                            ...cls
                        );
                        element.classList.remove(
                            ...ncls
                        );
                    } else {
                        //console.log("removed", ...element.getAttribute("view-class").split(" "));
                        element.classList.remove(
                            ...cls
                        );
                        element.classList.add(
                            ...ncls
                        );
                    }
                } catch (e) {
                
                }
                
            });
        },
        {
            root: null,
            rootMargin: margin+"px",
            threshold: [1.0, 0.0],
        },
    )).observe(element);
};


function markdown(text) {
    
}
