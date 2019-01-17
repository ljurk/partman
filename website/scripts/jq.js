
window.onload = function() {
var spans = document.getElementsByTagName("span"),
        index,
        span;

for (index = 0; index < spans.length; ++index) {
        span = spans[index];
        if (span.contentEditable) {
                  span.onblur = function() {
                      var text = this.innerHTML;
                      //text = text.replace(/&/g, "&amp").replace(/</g, "&lt;");
                      display("Content committed, span " +
                          this.id +
                          ": '" +
                          text + String(index) + "'");
                            };
                }
      }

function display(msg) {
        var p = document.createElement('p');
        p.innerHTML = msg;
        document.body.appendChild(p);
      }
};
