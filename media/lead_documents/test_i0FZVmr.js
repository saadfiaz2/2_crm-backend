import React, { useState, useEffect } from "react";
import Select from "react-select";
import axios from "axios";
import { BASE_URL } from "../../../constants/urls";

const EditLeads = ({ leadData }) => {
  const [leadName, setLeadName] = useState("");
  const [leadGenManager, setLeadGenManager] = useState(null);
  const [status, setStatus] = useState(null);
  const [source, setSource] = useState(null);
  const [sources, setSources] = useState([]);
  const [connects, setConnects] = useState(0);
  const [medium, setMedium] = useState(null);
  const [mediums, setMediums] = useState([]);
  const [assignedTo, setAssignedTo] = useState(null);
  const [accountExecutive, setAccountExecutive] = useState(null);
  const [sdr, setSdr] = useState(null);
  const [gora, setGora] = useState("");
  const [notes, setNotes] = useState("");
  const [users, setUsers] = useState([]);
  const [dl, setDL] = useState([]);

  const statusOptions = [
    { value: 1, label: "Contacted" },
    { value: 2, label: "Not Contacted" },
    { value: 3, label: "Closed" },
    { value: 4, label: "Lost" },
  ];

  useEffect(() => {
    if (leadData) {
      setLeadName(leadData.name || "");
      setLeadGenManager(leadData.leadGenManager || null);
      setStatus(leadData.status || null);
      setSource(leadData.source || null);
      setConnects(leadData.connects || 0);
      setMedium(leadData.medium || null);
      setAssignedTo(leadData.assignedTo || null);
      setAccountExecutive(leadData.accountExecutive || null);
      setSdr(leadData.sdr || null);
      setGora(leadData.gora || "");
      setNotes(leadData.notes || "");
    }
  }, [leadData]);

  useEffect(() => {
    const authToken = localStorage.getItem("BearerToken");

    const fetchMediums = async () => {
      try {
        const response = await axios.get(`${BASE_URL}mediums/`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        setMediums(
          response.data.map((medium) => ({
            value: medium.id,
            label: medium.name,
          }))
        );
      } catch (error) {
        console.error("Error fetching mediums:", error);
      }
    };

    const fetchSources = async () => {
      try {
        const response = await axios.get(`${BASE_URL}sources/`, {
          headers: { Authorization: `Bearer ${authToken}` },
        });
        setSources(
          response.data.map((src) => ({ value: src.id, label: src.name }))
        );
      } catch (error) {
        console.error("Error fetching sources:", error);
      }
    };

    fetchMediums();
    fetchSources();
  }, []);

  const fetchUsers = async () => {
    const authToken = localStorage.getItem("BearerToken");

    try {
      const response = await fetch(`${BASE_URL}users/by-role/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ roles: ["Admin"] }),
      });
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const fetchDLs = async () => {
    const authToken = localStorage.getItem("BearerToken");

    try {
      const response = await fetch(`${BASE_URL}users/by-role/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${authToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ roles: ["Employee"] }),
      });
      const data = await response.json();
      setDL(data);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  useEffect(() => {
    fetchUsers();
    fetchDLs();
  }, []);

  const leadGenManagerOptions = users.map((user) => ({
    value: user.id,
    label: user.username,
  }));
  const DLsOptions = dl.map((user) => ({
    value: user.id,
    label: user.username,
  }));

  const handleEditLead = async (e) => {
    e.preventDefault();
    const leadUpdateData = {
      name: leadName,
      lead_gen_manager_id: leadGenManager?.value,
      source_id: source?.value,
      connects: connects,
      medium_id: medium?.value,
      assigned_to_id: assignedTo?.value,
      account_executive_id: accountExecutive?.value,
      sdr_id: sdr?.value,
      gora: gora,
      communication_notes: notes,
    };

    try {
      const authToken = localStorage.getItem("BearerToken");
      const response = await axios.put(
        `${BASE_URL}leads/${leadData.id}/`,
        leadUpdateData,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Lead updated successfully:", response.data);
    } catch (error) {
      console.error("Error updating lead:", error);
    }
  };

  return (
    <div
      className="modal custom-modal fade custom-modal-two modal-padding"
      id="edit_leads"
      role="dialog"
    >
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header header-border justify-content-between p-0">
            <h5 className="modal-title">Edit Lead</h5>
            <button
              style={{ backgroundColor: "#667eea", borderColor: "white" }}
              type="button"
              className="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            >
              <span style={{ color: "white" }}>x</span>
            </button>
          </div>
          <div className="modal-body p-0">
            <form onSubmit={handleEditLead}>
              <div className="contact-input-set">
                <div className="row">
                  <div className="col-md-6">
                    <label>Lead Name</label>
                    <input
                      type="text"
                      value={leadName}
                      onChange={(e) => setLeadName(e.target.value)}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Lead Gen Manager</label>
                    <Select
                      value={leadGenManager}
                      onChange={setLeadGenManager}
                      options={leadGenManagerOptions}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Status</label>
                    <Select
                      value={status}
                      onChange={setStatus}
                      options={statusOptions}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Source</label>
                    <Select
                      value={source}
                      onChange={setSource}
                      options={sources}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Connects</label>
                    <input
                      type="number"
                      value={connects}
                      onChange={(e) => setConnects(e.target.value)}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Medium</label>
                    <Select
                      value={medium}
                      onChange={setMedium}
                      options={mediums}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Assigned To</label>
                    <Select
                      value={assignedTo}
                      onChange={setAssignedTo}
                      options={leadGenManagerOptions}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Account Executive</label>
                    <Select
                      value={accountExecutive}
                      onChange={setAccountExecutive}
                      options={leadGenManagerOptions}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>SDR</label>
                    <Select
                      value={sdr}
                      onChange={setSdr}
                      options={leadGenManagerOptions}
                      required
                    />
                  </div>

                  <div className="col-md-6">
                    <label>Gora</label>
                    <input
                      type="text"
                      value={gora}
                      onChange={(e) => setGora(e.target.value)}
                      required
                    />
                  </div>

                  <div className="col-md-12">
                    <label>Notes</label>
                    <textarea
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                      required
                    />
                  </div>

                  <div className="col-md-12">
                    <button type="submit">Save Lead</button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditLeads;
