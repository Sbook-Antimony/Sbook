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

class User {
    constructor(id, data) {
        this.id = id;
        this.collected = false;
        this.#data = data;
    }
    collect(callback) {
        return new Promise(function(resolve) {
            $.ajax({
                dataType: "json",
                url: `/users/${this.id}.json`,
                data: null,
                success: function(data) {
                    if(data.ok) {
                        this.#data = data;
                        this.collected = true;
                        if(callback) callback(data);
                        resolve(true);
                    } else {
                        resolve(false);
                    }
                }
            });
        });
    }
    name() {
        return this.#data.name;
    }
}
