class ModelInter {
    constructor(data) {
        this.data = data;
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
    static get(id, $scope, $http) {
        $http.get(`/users/${id}.json`).then(function(res) {
            let data = res.data;
            if(data.ok) {
                $scope.user = new User(data.user);
                window.user = $scope.user;
            } else {
            }
        });
    }
    constructor(data) {
        super(data);
        this.name =  data.name;
        this.profile = `/users/${this.data.id}/profile.png`;
        this.bio = data.bio;
        this.bio_html = data.bio_html;
    }
    modified() {
        return (
            this.name != this.data.name ||
            this.bio != this.data.bio
        )
    }
    save() {
        jQuery.ajax({
            url: '/settings/profile/submit/',
            success: function(data) {
                flashMessage("green", "Updated profile succesfuly");
            },
            error: function(zer) {
                flashMessage("red" , "Could not save question");
            },
            type: 'POST',
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
        bgColor : 'stat',              // Background color for toast
        textColor : '#fff',            // text color
        allowToastClose : false,       // Show the close button or not
        hideAfter : 5000,              // `false` to make it sticky or time in miliseconds to hide after
        stack : 5,                     // `fakse` to show one stack at a time count showing the number of toasts that can be shown at once
        textAlign : 'left',            // Alignment of text i.e. left, right, center
        position : 'bottom-right'       // bottom-left or bottom-right or bottom-center or top-left or top-right or top-center or mid-center or an object representing the left, right, top, bottom values to position the toast on page
    });
}
