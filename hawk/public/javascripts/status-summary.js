//======================================================================
//                        HA Web Konsole (Hawk)
// --------------------------------------------------------------------
//            A web-based GUI for managing and monitoring the
//          Pacemaker High-Availability cluster resource manager
//
// Copyright (c) 2009-2011 Novell Inc., Tim Serong <tserong@novell.com>
//                        All Rights Reserved.
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of version 2 of the GNU General Public License as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it would be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
//
// Further, this software is distributed without any warranty that it is
// free of the rightful claim of any third person regarding infringement
// or the like.  Any license provided herein, whether implied or
// otherwise, applies only to this software file.  Patent licenses, if
// any, provided herein do not apply to combinations of this program with
// other software, or any other product whatsoever.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write the Free Software Foundation,
// Inc., 59 Temple Place - Suite 330, Boston MA 02111-1307, USA.
//
//======================================================================

var summary_view = {
  active_detail: null,
  create: function() {
    var self = this;
    // Summary needs to show:
    // stonith enabled
    // no quorum policy
    // symmetric
    // stickiness(?)
    // maintenance mode
    $("#content").prepend($(
      // TODO(must): Localize
      '<div id="summary" style="display: none;" class="ui-corner-all">' +
        '<h1>Summary</h1>' +
        '<div id="confsum" class="summary">' +
          '<h2><a><img class="action-icon" alt="" /></a><span id="confsum-label">' + GETTEXT.summary_label() + "</span></h2>" +
          '<table cellpadding="0" cellspacing="0">' +
            '<tr id="confsum-stonith-enabled"><td>STONITH Enabled:</td><td></td></tr>' +
            '<tr id="confsum-no-quorum-policy"><td>No Quorum Policy:</td><td></td></tr>' +
            '<tr id="confsum-symmetric-cluster"><td>Symmetric Cluster:</td><td></td></tr>' +
            '<tr id="confsum-default-resource-stickiness"><td>Resource Stickiness:</td><td></td></tr>' +
            '<tr id="confsum-maintenance-mode"><td>Maintenance Mode:</td><td></td></tr>' +
          "</table>" +
        "</div>" +
        '<div id="nodesum" class="summary">' +
          '<h2 id="nodesum-label"></h2>' +
          '<table cellpadding="0" cellspacing="0">' +
            '<tr id="nodesum-pending" class="ns-transient clickable"><td>' + GETTEXT.node_state_pending() + ":</td><td></td></tr>" +
            '<tr id="nodesum-online" class="ns-active clickable"><td>' + GETTEXT.node_state_online() + ":</td><td></td></tr>" +
            '<tr id="nodesum-standby" class="ns-inactive clickable"><td>' + GETTEXT.node_state_standby() + ":</td><td></td></tr>" +
            '<tr id="nodesum-offline" class="ns-inactive clickable"><td>' + GETTEXT.node_state_offline() + ":</td><td></td></tr>" +
            '<tr id="nodesum-unclean" class="ns-error clickable"><td>' + GETTEXT.node_state_unclean() + ":</td><td></td></tr>" +
          "</table>" +
        "</div>" +
        '<div id="ressum" class="summary">' +
          '<h2><a><img class="action-icon" alt="" /></a><span id="ressum-label"></span></h2>' +
          '<table cellpadding="0" cellspacing="0">' +
            '<tr id="ressum-pending" class="rs-transient clickable"><td>Pending:</td><td></td></tr>' +
            '<tr id="ressum-started" class="rs-active clickable"><td>Started:</td><td></td></tr>' +
            '<tr id="ressum-master" class="rs-master clickable"><td>Master:</td><td></td></tr>' +
            '<tr id="ressum-slave" class="rs-slave clickable"><td>Slave:</td><td></td></tr>' +
            '<tr id="ressum-stopped" class="rs-inactive clickable"><td>Stopped:</td><td></td></tr>' +
          "</table>" +
        "</div>" +
      "</div>" +
      '<div id="details" style="display: none;" class="ui-corner-all">' +
        '<div style="float: right;"><button type="button" style="border: none; background: none; font-size: 0.7em; margin-right: -0.5em;">Close</button></div><h1>Details</h1>' +
        '<div id="itemlist"></div>' +
      "</div>"));
    $("#summary").find("tr").each(function() {
      $(this).hide();
      if ($(this).hasClass("clickable")) {
        $(this).css("textDecoration", "underline");
        $(this).click(function() {
          self.active_detail = $(this).attr("id");
          $("#itemlist").children().hide();
          $("#itemlist").children("." + self.active_detail).show();
          $("#details").show();
        });
      }
    });
    $("#details").find("button").button({
      text: false,
      icons: {
        primary: "ui-icon-close"
      }
    }).click(function() {
        $("#details").hide();
        self.active_detail = null;
    });
    // Menu setup cribbed from jquery.ui.panel
    var ma = $("#summary").find("a");
    var mi = ma.children(":first");
    mi.attr("src", url_root + "/images/icons/edit.png");
    mi.attr("alt", GETTEXT.configure());
    mi.attr("title", GETTEXT.configure());
    ma.attr("href", url_root + "/cib/live/crm_config/cib-bootstrap-options/edit");
    ma.click(function(event) {
      event.stopPropagation();
    });
    ma = $("#ressum").find("a");
    mi = ma.children(":first");
    mi.attr("src", url_root + "/images/icons/properties.png");
    ma.click(function(event) {
      return $(jq("menu::reslist")).popupmenu("popup", $(this));
    });
  },
  destroy: function() {
    // NYI
  },
  update: function() {
    var self = this;

    $("#summary").show();
    $.each(["stonith-enabled", "no-quorum-policy", "symmetric-cluster",
            "default-resource-stickiness", "maintenance-mode"], function() {
      var p = this.toString();
      if (cib.crm_config[p] != null) {
        $("#confsum-" + p).show().children(":last").html(escape_html(cib.crm_config[p].toString()));
      } else {
        $("#confsum-" + p).hide();
      }
    });
    // Special case for important highlights
    if (cib.crm_config["stonith-enabled"]) {
      $("#confsum-stonith-enabled").removeClass("rs-error");
    } else {
      $("#confsum-stonith-enabled").addClass("rs-error");
    }
    if (cib.crm_config["maintenance-mode"]) {
      $("#confsum-maintenance-mode").addClass("rs-transient");
    } else {
      $("#confsum-maintenance-mode").removeClass("rs-transient");
    }

    // Rebuild item list each time
    $("#itemlist").children().remove();

    $("#nodesum-label").html(escape_html(GETTEXT.nodes_configured(cib.nodes.length)));
    self._zero_counters("#nodesum");
    $.each(cib.nodes, function() {
      self._increment_counter("#nodesum-" + this.state);
      // Switch cribbed from _cib_to_nodelist_panel()
      var className;
      var label = GETTEXT.node_state_unknown();
      switch (this.state) {
        case "online":
          className = "active nodesum-online";
          label = GETTEXT.node_state_online();
          break;
        case "offline":
          className = "inactive nodesum-offline";
          label = GETTEXT.node_state_offline();
          break;
        case "pending":
          className = "transient nodesum-pending";
          label = GETTEXT.node_state_pending();
          break;
        case "standby":
          className = "inactive nodesum-standby";
          label = GETTEXT.node_state_standby();
          break;
        case "unclean":
          className = "error nodesum-unclean";
          label = GETTEXT.node_state_unclean();
          break;
      }
      var display = 'none';
      if (self.active_detail && className.indexOf(self.active_detail) >= 0) {
        display = "auto";
      }
      var d = new_item_div("node::" + this.uname);
      d.attr("class", "ui-corner-all node ns-" + className).css("display", display);
      d.find("span").html(escape_html(GETTEXT.node_state(this.uname, label)));
      $("#itemlist").append(d);
      if (!cib_file) {
        add_mgmt_menu($(jq("node::" + this.uname + "::menu")));
      }
    });
    self._show_counters("#nodesum");

    $("#ressum-label").html(escape_html(GETTEXT.resources_configured(resource_count)));
    self._zero_counters("#ressum");
    $.each(resources_by_id, function() {
      if (!this.instances) return;
      var res_id = this.id;
      $.each(this.instances, function(k) {
        var id = res_id;
        if (k != "default") {
          id += ":" + k;
        }
        // Display logic same as _get_primitive()
        var status_class = "res-primitive";
        var label = "";
        if (this.master) {
          self._increment_counter("#ressum-master");
          label = GETTEXT.resource_state_master(id, this.master);
          status_class += " rs-active rs-master ressum-master";
        } else if (this.slave) {
          self._increment_counter("#ressum-slave");
          label = GETTEXT.resource_state_slave(id, this.slave);
          status_class += " rs-active rs-slave ressum-slave";
        } else if (this.started) {
          self._increment_counter("#ressum-started");
          label = GETTEXT.resource_state_started(id, this.started);
          status_class += " rs-active ressum-started";
        } else if (this.pending) {
          self._increment_counter("#ressum-pending");
          label = GETTEXT.resource_state_pending(id, this.pending);
          status_class += " rs-transient ressum-pending";
        } else {
          self._increment_counter("#ressum-stopped");
          label = GETTEXT.resource_state_stopped(id);
          status_class += " rs-inactive ressum-stopped";
        }
        var display = 'none';
        if (self.active_detail && status_class.indexOf(self.active_detail) >= 0) {
          display = "auto";
        }
        var d = new_item_div("resource::" + id);
        d.attr("class", "ui-corner-all " + status_class).css("display", display);
        d.find("span").html(escape_html(label));
        $("#itemlist").append(d);
        flag_error("resource::" + id, this.failed_ops);
        if (!cib_file) {
          add_mgmt_menu($(jq("resource::" + id + "::menu")));
        }
      });
    });
    self._show_counters("#ressum");

    // Hide item list if there's nothing to show
    if ($("#itemlist").children(":visible").length == 0) {
      $("#details").hide();
      self.active_detail = null;
    }
  },
  hide: function() {
    $("#summary").hide();
    $("#details").hide();
    $("#itemlist").children().remove();
    this.active_detail = null;
  },
  _zero_counters: function(parent_id) {
    $(parent_id).children("table").find("tr").each(function() {
      $(this).children(":last").text("0");
    });
  },
  _increment_counter: function(row_id) {
    $(row_id).children(":last").text(parseInt($(row_id).children(":last").text()) + 1);
  },
  _show_counters: function(parent_id) {
    $(parent_id).children("table").find("tr").each(function() {
      if (parseInt($(this).children(":last").text())) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  }
};

