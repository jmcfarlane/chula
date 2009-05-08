/* Simple client for the Github api 
 *
 */

// Class constructor
RF.Github = function (username, repo) {
  this.username = username;
  this.repo = repo;
  this.transport = 'json';
  this.version = 'v1';
  this.baseurl = 'http://github.com/api';
}

// Fetch commit list
RF.Github.prototype.commits = function (branch, callback, max) {
  // Set the maximum number of commits to show
  if (isNaN(max)) {
    this.max = 10;
  } else {
    this.max = max;
  }

  // Create the api call to make
  var url = new Array();
  url.push(this.baseurl);
  url.push(this.version);
  url.push(this.transport);
  url.push(this.username);
  url.push(this.repo);
  url.push('commits');
  url.push(branch);
  url.push('?callback=' + callback);

  // Call the api including the specified callback
  this.fetch(url.join('/'));
}

// Process commit list (callback)
RF.Github.prototype.commits_cb = function (json) {
  var commits = json.commits;
  var fragment = document.createDocumentFragment();
  var list = document.createElement('ul');

  for (i=0; i<commits.length; i++) {
    var commit = commits[i];
    //console.log(commit.message)
    //console.log(commit.author.name)
    //console.log(commit.authored_date)
    //console.log(commit.committed_date)
    //console.log(commit.id)
    //console.log(commit.url)

    // Calculate how many hours ago this commit was
    var ms = (new Date()) - this.str2date(commit.committed_date);
    var hours = parseInt(ms / 1000 / 60 / 60);
    
    // Create the text to display
    var msg = commit.message.substr(0, commit.message.search(/\n/))
    if (msg == '') {
      msg = commit.message;
    }

    // Create a list_element and anchor
    var list_element = document.createElement('li');
    var anchor = document.createElement('a');
    anchor.setAttribute('href', commit.url);
    anchor.innerHTML = msg;
    
    // Include detail about the commit
    var detail = document.createElement('span');
    html = ' ('+ hours +' hours ago, by: ' + commit.author.name + ')'
    detail.innerHTML = html;

    // Add list element to the list
    list_element.appendChild(anchor);
    list_element.appendChild(detail);
    list.appendChild(list_element);

    // Set the max number of commits to show
    if (i >= this.max - 1) {
      break;
    }
  }

  // Add the list to the fragment
  fragment.appendChild(list);

  // Clear the progress indicator and add the fragment to the dom
  var obj = document.getElementById('commits');
  obj.innerHTML = '';
  obj.appendChild(fragment);
}

// Format Github timestamps (2009-04-24T19:41:48-07:00)
RF.Github.prototype.str2date = function (input) {
  parts = input.replace(/T/, ' ').split(/ /);
  ymd = parts[0].split(/-/);
  ymd = ymd[1] + '/' + ymd[2] + '/' + ymd[0]
  time = parts[1];

  return new Date(ymd + ' ' + time);
}

// Make an github api call
RF.Github.prototype.fetch = function (url) {
  var script = document.createElement('script')
  script.setAttribute('src', url);
  document.getElementsByTagName('head')[0].appendChild(script);
}
