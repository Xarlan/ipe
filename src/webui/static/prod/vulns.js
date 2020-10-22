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
/******/ 	return __webpack_require__(__webpack_require__.s = 2);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/vulns.js":
/*!*************************!*\
  !*** ./src/js/vulns.js ***!
  \*************************/
/*! no static exports found */
/***/ (function(module, exports) {

var vuln_add_btn = document.getElementsByClassName("vuln__add-btn")[0];
var create_report_vuln_btn = document.getElementById("report-per-vuln");
var create_report_host_btn = document.getElementById("report-per-host");
var create_report_user_btn = document.getElementById("report-for-user");
vuln_add_btn.addEventListener("click", function (event) {
  event.preventDefault();
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

  fetch(SERVER_PROTO + SERVER_HOST + "/api/createVulnerability", {
    method: "post",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      project_id: project_id,
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
      request: request,
      response: response,
      target: hosts && hosts.length && hosts.length > 0 ? hosts : []
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
create_report_user_btn.addEventListener("click", function (event) {
  event.preventDefault();
  var form = document.createElement("form");
  form.className = "report__form";
  form.setAttribute("action", SERVER_PROTO + SERVER_HOST + "/report/user/" + project_id);
  form.setAttribute("target", "_blank");
  document.body.append(form);
  form.submit();
});
create_report_vuln_btn.addEventListener("click", function (event) {
  event.preventDefault();
  var form = document.createElement("form");
  form.className = "report__form";
  form.setAttribute("action", SERVER_PROTO + SERVER_HOST + "/report/vuln/" + project_id);
  form.setAttribute("target", "_blank");
  document.body.append(form);
  form.submit();
});
create_report_host_btn.addEventListener("click", function (event) {
  event.preventDefault();
  var form = document.createElement("form");
  form.className = "report__form";
  form.setAttribute("action", SERVER_PROTO + SERVER_HOST + "/report/host/" + project_id);
  form.setAttribute("target", "_blank");
  document.body.append(form);
  form.submit();
});

/***/ }),

/***/ 2:
/*!*******************************!*\
  !*** multi ./src/js/vulns.js ***!
  \*******************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! ./src/js/vulns.js */"./src/js/vulns.js");


/***/ })

/******/ });
//# sourceMappingURL=vulns.js.map