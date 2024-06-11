class MarkdownText {
    constructor(text) {
        this.text = text;
    }
    html() {
        $.jQuery.ajax({
          url: '/markdown',
          type: 'POST',
          dataType: 'xml/html/script/json/jsonp',
          data: {param1: 'value1'},
          complete: function(xhr, textStatus) {
            //called when complete
          },
          success: function(data, textStatus, xhr) {
            //called when successful
          },
          error: function(xhr, textStatus, errorThrown) {
            //called when there is an error
          }
        });

    }
}

class ModelInter {
    constructor(id) {
        this.id = id;
    }
}
class User extends ModelInter {
    static from_id(id) {
        return new Promise(function(resolve) {
            $.ajax({
                dataType: "json",
                url: `/users/${this.id}.json`,
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
    constructor(data) {
        this.data = data;
    }
    name() {
        return this.#data.name;
    }
}

