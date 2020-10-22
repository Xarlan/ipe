/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 3);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/vuln.js":
/*!************************!*\
  !*** ./src/js/vuln.js ***!
  \************************/
/*! no static exports found */
/***/ (function(module, exports) {

var vuln_delete_btn = document.getElementsByClassName("vuln__delete-btn")[0];
var vuln_edit_btn = document.getElementsByClassName("vuln__edit-btn")[0];
var attach_upload_btn = document.getElementsByClassName("attach__upload")[0];
vuln_delete_btn.addEventListener("click", function () {
  var is_delete = confirm("Are you sure you want to delete vuln ?");

  if (is_delete) {
    fetch(SERVER_PROTO + SERVER_HOST + "/api/deleteVulnerability", {
      method: "post",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        vuln_id: vuln_id
      })
    }).then(function (response) {
      return response.json();
    }).then(function (data) {
      if (data.status === 1) {
        window.location = SERVER_PROTO + SERVER_HOST + "/project/" + project_id;
      } else {
        alert(data.error);
      }
    })["catch"](function (error) {
      return alert(error);
    });
  }
});
vuln_edit_btn.addEventListener("click", function () {
  var name = document.querySelector("input[name=name]").value;
  var full_path = document.querySelector("input[name=full_path]").value;
  var description = document.querySelector("textarea[name=description]").value;
  var risk = document.querySelector("textarea[name=risk]").value;
  var details = document.querySelector("textarea[name=details]").value;
  var recommendation = document.querySelector("textarea[name=recommendation]").value;
  var context_elems = document.getElementsByClassName("vuln__context"),
      checked_context;
  var criticality_inputs = document.querySelectorAll("input[name=criticality]"),
      checked_criticality;
  var probability_inputs = document.querySelectorAll("input[name=probability]"),
      checked_probability;
  var target = document.getElementById("vuln-target").value,
      hosts;
  var request = document.querySelector("textarea[name=request]").value;
  var response = document.querySelector("textarea[name=response]").value;

  if (target.length) {
    hosts = target.split(",").filter(function (host) {
      return host.trim().length > 0;
    }).map(function (host) {
      return host.trim();
    });
  }

  for (var i = 0; i < context_elems.length; i++) {
    if (context_elems[i].checked) {
      checked_context = context_elems[i].value;
    }
  }

  for (var _i = 0; _i < criticality_inputs.length; _i++) {
    if (criticality_inputs[_i].checked) {
      checked_criticality = criticality_inputs[_i].value;
    }
  }

  for (var _i2 = 0; _i2 < probability_inputs.length; _i2++) {
    if (probability_inputs[_i2].checked) {
      checked_probability = probability_inputs[_i2].value;
    }
  }

  fetch(SERVER_PROTO + SERVER_HOST + "/api/editVulnerability", {
    method: "post",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      project_id: project_id,
      vuln_id: vuln_id,
      name: name,
      object: checked_context,
      full_path: full_path,
      criticality: checked_criticality,
      probability: checked_probability,
      final_criticality: Math.floor((Number(checked_criticality) + Number(checked_probability)) / 2),
      description: description,
      risk: risk,
      details: details,
      recommendation: recommendation,
      target: hosts && hosts.length && hosts.length > 0 ? hosts : [],
      request: request,
      response: response
    })
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    if (data.status === 1) {
      window.location = "";
    } else {
      alert(data.error);
    }
  })["catch"](function (error) {
    return alert(error);
  });
});
var attach_number = 1;
var create_item_flag = [];

window.handle_attach = function (target) {
  var attach_item = target.closest("li");
  attach_item.querySelector(".attach__name").innerText = target.files[0].name;

  if (!create_item_flag.includes(target.id)) {
    create_item_flag.push(target.id);
    var attach_list = document.getElementsByClassName("attach__list")[0];
    var attach_clone = document.createElement('li');
    attach_number++;
    attach_clone.className = "attach__item";
    attach_clone.innerHTML = "<label for=\"uploadbtn-".concat(attach_number, "\" class=\"btn btn-outline-primary scope__add-btn uploadButton\">choose attach</label>\n                          <input class=\"attach__input\" type=\"file\" id=\"uploadbtn-").concat(attach_number, "\" accept=\".jpg,.jpeg,.png\" onchange=\"handle_attach(this)\">\n                          <input type=\"text\" id=\"attach__description\" class=\"attach__description form-control\" name=\"attach__description\" placeholder=\"description\">\n                          <span class=\"attach__name\"></span>\n                          <span class=\"attach__item-close disabled\" onclick=\"this.closest('li').parentNode.removeChild(this.closest('li'));\">X</span>");
    attach_list.appendChild(attach_clone);
  }

  if (attach_item.querySelector(".attach__item-close.disabled")) {
    attach_item.querySelector(".attach__item-close.disabled").classList.remove("disabled");
  }
};

attach_upload_btn.addEventListener("click", function () {
  var attaches = document.getElementsByClassName("attach__input");

  for (var i = 0; i < attaches.length; i++) {
    if (attaches[i].files[0]) {
      (function () {
        var attach_dom_el = attaches[i];
        var attach_description = attaches[i].closest(".attach__item").querySelector(".attach__description").value;
        var formData = new FormData();
        formData.append("attach", attaches[i].files[0]);
        formData.append("vuln_id", vuln_id);
        formData.append("description", attach_description);
        var uploaded_attach_block = document.getElementsByClassName("attach__existed")[0];
        fetch(SERVER_PROTO + SERVER_HOST + '/api/uploadFile', {
          method: "post",
          body: formData
        }).then(function (response) {
          return response.json();
        }).then(function (data) {
          if (data.status === 1) {
            var new_attach = document.createElement('li');
            new_attach.innerHTML = "<a href=\"/api/getAttach/".concat(data.id, "\" target=\"_blank\">").concat(data.filename, "</a> - <span>").concat(attach_description.replace(/&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/"/g, "&quot;"), "</span> - <button class=\"btn btn-outline-danger attach__delete\" onclick=\"delete_attach(event, ").concat(data.id, ")\">delete</button>");
            uploaded_attach_block.appendChild(new_attach);
            attach_dom_el.closest("li").parentNode.removeChild(attach_dom_el.closest('li'));
          } else {
            alert(data.error);
          }
        })["catch"](function (error) {
          return alert(error);
        });
      })();
    }
  }
});

window.delete_attach = function (event, id) {
  event.preventDefault();
  var is_delete = confirm("Are you sure you want to delete attachment ?");

  if (is_delete) {
    fetch(SERVER_PROTO + SERVER_HOST + "/api/deleteAttach/", {
      method: "post",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: id
      })
    }).then(function (response) {
      return response.json();
    }).then(function (data) {
      if (data.status === 1) {
        atta_item = event.target.closest("li");
        atta_item.parentNode.removeChild(atta_item);
      } else {
        alert(data.error);
      }
    })["catch"](function (error) {
      return alert(error);
    });
  }
};

/***/ }),

/***/ 3:
/*!******************************!*\
  !*** multi ./src/js/vuln.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! ./src/js/vuln.js */"./src/js/vuln.js");


/***/ })

/******/ });
//# sourceMappingURL=vuln.js.map