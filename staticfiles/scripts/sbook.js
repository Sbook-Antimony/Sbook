class ModelInter {
    constructor(data) {
        this.data = data;
        for(let key in data) this[key] = data[key];
    }
}
class User extends ModelInter {
    static from_id_async(id) {
        return new Promise(function(resolve) {
            $.ajax({
                dataType: "json",
                url: `/users/${id}.json`,
                data: null,
                success: function(data) {
                    if(data.ok) {
                        resolve(new User(data.user));
                    } else {
                        resolve(false);
                    }
                }
            });
        });
    }
    static get(id, $http, callback) {
        $http.get(`/users/${id}.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                callback(new User(data.user));
            }
        });
    }
    static get_current($http, callback) {
        $http.get(`/user.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                callback(new User(data.user));
            }
        });
    }
    get_classrooms_iter($http, callback) {
        let classrooms = [];
        for(let classroomid of this.data.classrooms) {
            Classroom.get(classroomid, $http, function(classroom) {
                callback(classroom);
            });
        }
    }
    constructor(data) {
        super(data);
        this.profile = `/users/${this.data.id}/profile.png`;
    }
    modified() {
        return (
            this.name != this.data.name ||
            this.bio != this.data.bio
        )
    }
    save(callback) {
        let user = this;
        jQuery.ajax({
            url: '/settings/profile/submit/',
            success: function(data) {
                flashMessage("green", "Updated profile succesfuly");
                user.data.bio = user.bio;
                user.data.name = user.name;
                if(callback) callback();
            },
            error: function(zer) {
                flashMessage("red" , "Could not save question");
            },
            type: 'GET',
            data: this.serialize(),
            dataType: 'JSON',
        });
    }
    serialize() {
        return {
            bio: this.bio,
            name: this.name,
        };
    }
}
class QuizzUser extends ModelInter {
    static from_id_async(id) {
        return new Promise(function(resolve) {
            jQuery.ajax({
                dataType: "json",
                url: `/quizz/users/${id}.json`,
                data: null,
                success: function(data) {
                    if(data.ok) {
                        resolve(new QuizzUser(data.user));
                    } else {
                        resolve(false);
                    }
                }
            });
        });
    }
    static get(id, $http, callback) {
        $http.get(`/quizz/users/${id}.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                callback(new QuizzUser(data.user));
            }
        });
    }
    constructor(data) {
        super(data);
        this.sbook = new User(data.sbook);
    }
}


class Classroom extends ModelInter {
    static get(id, $http, callback) {
        $http.get(`/school/classrooms/${id}.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                callback(new Classroom(data.classroom));
            } else {
                callback(null);
            }
        });
    }
}



class Question extends ModelInter {
    constructor(id, {question, options}) {
        let opts = {};
        if(options) for(let [k, v] of options) opts[k] = v;
        super({question, id, options: opts});
    }
    serialize() {
        let obj = {
            question: this.question,
            options: {},
        };
        for(let i = 0; i < this.options.length; i++) {
            obj.options[
                String.fromCodePoint(i+'A'.charCodeAt(0)).toString()
            ] = this.options[i].text;
        }
        return obj;
    }
    addOption(k, v) {
        if(Object.keys(this.options).length > 10) {
            flashMessage("#f63",`Oh, ${Object.keys(this.options).length} thats many options, don't you think?`);
            return;
        }
        if(k == null) k = String.fromCodePoint(
            Object.keys(this.options).length+'A'.charCodeAt(0)
        ).toString()
        this.options[k] = v;
    }
}
class Quizz extends ModelInter {
    static from_id_async(id) {
        return new Promise(function(resolve) {
            $.ajax({
                dataType: "json",
                url: `/quizz/quizzes/${id}.json`,
                data: null,
                success: function(data) {
                    if(data.ok) {
                        resolve(new Quizz(data.quizz));
                    } else {
                        resolve(false);
                    }
                }
            });
        });
    }
    static get(id, $http, callback) {
        $http.get(`/quizz/quizzes/${id}.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                callback(new Quizz(data.quizz));
            }
        });
    }
    static all($http, callback) {
        $http.get(`/quizz/quizzes.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                let quizzes = [];
                for(let qd of data.quizzes) {
                    quizzes.push(new Quizz(qd));
                }
                callback(quizzes);
            }
        });
    }
    constructor(data) {
        super(data);
        let i = 0;
        this.questions = data.questions.map((q) => new Question(i++ ,q));
        this.authors = data.authors.map((q) => new QuizzUser(q));
    }
    modified() {
        return (
            this.name != this.data.name ||
            this.bio != this.data.bio
        )
    }
    save(callback) {
        let user = this;
        jQuery.ajax({
            url: '/settings/profile/submit/',
            success: function(data) {
                flashMessage("green", "Updated profile succesfuly");
                user.data.bio = user.bio;
                user.data.name = user.name;
                if(callback) callback();
            },
            error: function(zer) {
                flashMessage("red" , "Could not save question");
            },
            type: 'GET',
            data: this.serialize(),
            dataType: 'JSON',
        });
    }
    serialize() {
        return {
            bio: this.bio,
            name: this.name,
        };
    }
}






function flashMessage(stat, text) {
    jQuery.toast({
        text : text,
        showHideTransition : 'slide',  // It can be plain, fade or slide
        bgColor : stat,              // Background color for toast
        textColor : '#fff',            // text color
        allowToastClose : false,       // Show the close button or not
        hideAfter : 5000,              // `false` to make it sticky or time in miliseconds to hide after
        stack : 5,                     // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign : 'left',            // Alignment of text i.e. left, right, center
        position : 'bottom-right'       // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
    });
}


setInterval(function() {
    for(let elt of document.getElementsByClassName('raw-markdown')) {
        if(!elt.innerHTML) {
            continue;
        }
        jQuery.ajax({
            url: '/markdown/',
            success: function(data) {
                console.log(data);
                if(data.ok) {
                    elt.innerHTML = data.html;
                    elt.classList.remove('raw-markdown');
                }
            },
            type: 'GET',
            data: {
                md: btoa(elt.innerHTML.trim()),
            },
            dataType: 'JSON',
        });
    }
}, 200);

