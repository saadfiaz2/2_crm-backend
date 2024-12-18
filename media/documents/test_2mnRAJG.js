import React, { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { Mail, Key, Link2 } from "react-feather";
import {
  Avatar_05,
  Avatar_10,
  Avatar_16,
} from "../../../../../Routes/ImagePath";
import { useLocation } from "react-router-dom";
import { BASE_URL } from "../../../../../constants/urls";

const ProjectDetails = () => {
  const companies = useMemo(
    () => [
      { value: 1, label: "Fintech" },
      { value: 2, label: "Block chain" },
      { value: 3, label: "Real Estate" },
      { value: 4, label: "Game development" },
      { value: 5, label: "Education and research" },
      { value: 6, label: "Logistics and transformation" },
      { value: 7, label: "Health care" },
      { value: 8, label: "Retail and distribution" },
      { value: 9, label: "E-Commerce" },
      { value: 10, label: "Artificial Intelligence" },
    ],
    []
  );

  const location = useLocation();

  const [teamMemberOptions, setTeamMemberOptions] = useState([]);
  const [teamLeaderOptions, setTeamLeaderOptions] = useState([]);
  const [techStackOptions, setTechStackOptions] = useState([]);
  const [stacks, setStacks] = useState();
  const [platformOptions, setPlatformOptions] = useState([]);
  const [team, setTeam] = useState();
  const { project } = location.state || {};

  // const handleDownload = (fileURL, fileName) => {
  //   const url = fileURL;
  //   const link = document.createElement("a");
  //   link.href = url;
  //   link.setAttribute("download", fileName);
  //   document.body.appendChild(link);
  //   link.click();
  //   link.remove();
  //   console.log(team);
  // };

  useEffect(() => {
    const authToken = localStorage.getItem("BearerToken");
    const fetchPlatforms = async () => {
      try {
        const response = await fetch(`${BASE_URL}platforms/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        const data = await response.json();

        const options = data.map((platform) => ({
          value: platform.id,
          label: platform.name,
        }));

        setPlatformOptions(options);
      } catch (error) {
        console.error("Error fetching platforms:", error);
      }
    };

    fetchPlatforms();
  }, []);

  useEffect(() => {
    const fetchTeamMembers = async () => {
      const authToken = localStorage.getItem("BearerToken");
      try {
        const response = await fetch(`${BASE_URL}users/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        const data = await response.json();
        const options = data.map((user) => ({
          value: user.id,
          label: user.username,
        }));
        setTeamMemberOptions(options);
        setTeamLeaderOptions(options);
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    fetchTeamMembers();
  }, []);

  useEffect(() => {
    const authToken = localStorage.getItem("BearerToken");
    const fetchTechStacks = async () => {
      try {
        const response = await fetch(`${BASE_URL}techstacks/`, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });
        const data = await response.json();

        const options = data.map((stack) => ({
          value: stack.id,
          label: stack.name,
        }));

        setTechStackOptions(options);
      } catch (error) {
        console.error("Error fetching tech stacks:", error);
      }
    };

    fetchTechStacks();
  }, []);

  useEffect(() => {
    try {
      const tech_stack = techStackOptions
        .filter((option) => project.tech_stack.includes(option.value))
        .map((option) => option.label);
      setStacks(tech_stack);

      setTeam(
        teamLeaderOptions
          .filter((option) => project.development_team.includes(option.value))
          .map((option) => option.label)
      );
    } catch {
      console.log("not edit");
    }
  }, [project, techStackOptions, teamLeaderOptions]);

  useEffect(() => {
    try {
      const selected = platformOptions.filter((option) =>
        project.platform.includes(option.value)
      );
      const tech_selected = techStackOptions.filter((option) =>
        project.tech_stack.includes(option.value)
      );
      const dev_team = teamMemberOptions.filter((option) =>
        project.development_team.includes(option.value)
      );

      const person = teamMemberOptions.filter(
        (option) => option.label === project.responsible_person
      );

      const ind = companies.find(
        (company) =>
          company.label.toLowerCase() === project.industry.toLowerCase()
      );

      // Setting various state values
      setProjectName(project.name);
      setClientName(project.client_name);
      setGithubLink(project.git_link);
      setLiveLink(project.live_link);
      setFigmaLink(project.figma_link);
      setServerLoginEmail(project.server_email);
      setServerLoginPassword(project.server_password);
      setTeamLeader(person);
      setTeamMembers(dev_team);
      setDescription(project.description);
      setPlatforms(selected);
      setTechStack(tech_selected);
      setIndustry(ind);
      setLogo(project.logo_icon);
      setProjectDuration(project.project_duration);
      setServerLink(project.server_link);
      setRating(parseInt(project.rating));
    } catch {
      console.log("not edit");
    }
  }, [
    project,
    teamMemberOptions,
    companies,
    platformOptions,
    techStackOptions,
  ]);

  const handleOpenInNewTab = (fileURL) => {
    window.open(fileURL, "_blank", "noopener,noreferrer");
  };

  return (
    <>
      <div>
        <div className="page-wrapper">
          <div className="content container-fluid">
            <div className="row">
              <div className="col-md-12">
                <div className="contact-head">
                  <div className="row align-items-center">
                    <div className="col">
                      <ul className="contact-breadcrumb">
                        <li>
                          <Link to="/file-manager">
                            <i className="las la-arrow-left" />
                            File Manager
                          </Link>
                        </li>
                        <li>{project?.name || ""}</li>

                        <Link
                          to="#"
                          className="action-icon "
                          style={{
                            marginLeft: "80%",
                          }}
                          data-bs-toggle="dropdown"
                          aria-expanded="false"
                        >
                          <i className="material-icons ">more_vert</i>
                        </Link>
                        <div className="dropdown-menu dropdown-menu-right ">
                          <Link
                            className="dropdown-item"
                            to="#"
                            data-bs-toggle="modal"
                            data-bs-target="#edit_project"
                          >
                            <i className="fa fa-pencil m-r-5" /> Edit
                          </Link>
                          <Link
                            className="dropdown-item"
                            to="#"
                            data-bs-toggle="modal"
                            data-bs-backdrop="static"
                            data-bs-target="#delete"
                          >
                            <i className="fa fa-trash m-r-5" /> Delete
                          </Link>
                        </div>
                      </ul>
                    </div>
                  </div>
                </div>
                <div className="contact-wrap">
                  <div className="contact-profile">
                    <div className="avatar avatar-xxl">
                      <img
                        src={project?.logo_icon || ""}
                        alt="Project Logo"
                        style={{
                          width: "100px",
                          height: "100px",
                          objectFit: "cover",
                        }}
                      />
                      <span className="status online" />
                    </div>
                    <div className="name-user">
                      <h4>{project?.name || ""}</h4>
                      <p>{project?.client_name || ""}</p>
                      <div className="badge-rate">
                        <span className="badge badge-light">
                          {project?.industry || ""}
                        </span>
                        <p>
                          <i className="fa-solid fa-star" />
                          {project?.rating || ""}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="contacts-action">
                    <ul className="social-info">
                      <li>
                        <Link
                          to={project?.git_link || ""}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <i className="fa-brands fa-github" />
                        </Link>
                      </li>
                      {"    "}
                      <li>
                        <Link
                          to={project?.figma_link || ""}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <i className="fa-brands fa-figma" />
                        </Link>
                      </li>
                      {"    "}
                      <li>
                        <Link
                          to={project?.live_link || ""}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <i className="fa-brands fa-chrome" />
                        </Link>
                      </li>
                      {"    "}
                    </ul>
                  </div>
                </div>
              </div>
              <div className="col-xl-3">
                <div className="stickybar">
                  <div className="card contact-sidebar">
                    <h5>Project Information</h5>
                    <ul className="other-info">
                      <li>
                        <span className="other-title">Team Lead:</span>
                        <ul className="team-members">
                          <li>
                            <Link
                              to="#"
                              data-bs-toggle="tooltip"
                              title="Jeffery Lalor"
                              style={{ pointerEvents: "none" }}
                            >
                              <img alt="" src={Avatar_16} />
                            </Link>
                          </li>
                        </ul>
                      </li>
                      <li>
                        <span className="other-title">Team Members:</span>
                        <ul className="team-members">
                          <li>
                            <Link
                              //to="#"
                              data-bs-toggle="tooltip"
                              title="John Smith"
                              style={{ pointerEvents: "none" }}
                            >
                              <img alt="" src={Avatar_10} />
                            </Link>
                          </li>
                          <li>
                            <Link
                              //to="#"
                              data-bs-toggle="tooltip"
                              title="Mike Litorus"
                              style={{ pointerEvents: "none" }}
                            >
                              <img alt="" src={Avatar_05} />
                            </Link>
                          </li>
                          <li className="dropdown avatar-dropdown">
                            <Link
                              // to="#"
                              className="all-users dropdown-toggle"
                              data-bs-toggle="dropdown"
                              aria-expanded="false"
                              style={{ pointerEvents: "none" }}
                            >
                              +15
                            </Link>
                          </li>
                        </ul>
                      </li>
                      <li>
                        <span className="other-title">Tech Stack:</span>
                        <span>{stacks}</span>
                      </li>
                      <li>
                        <span className="other-title">Platform:</span>
                        <span>{project?.platforms || ""}</span>
                      </li>
                      <li>
                        <span className="other-title">Project Duration:</span>
                        <span>{project?.project_duration || ""}</span>
                      </li>
                    </ul>
                    <h5>Server Information</h5>
                    <ul className="basic-info">
                      <li>
                        <span>
                          <Mail size={15} />
                        </span>
                        <p>{project?.server_email || ""}</p>
                      </li>
                      <li>
                        <span>
                          <Key size={15} />
                        </span>
                        <p>{project?.server_password || ""}</p>
                      </li>
                      <li>
                        <span>
                          <Link2 size={15} />
                        </span>
                        <a
                          href={project?.server_link || ""}
                          target="_blank"
                          rel="noopener noreferrer"
                          style={{ cursor: "pointer" }}
                        >
                          {project?.server_link || ""}
                        </a>
                      </li>
                    </ul>

                    <ul className="other-info">
                      {project?.documents && project?.documents.length > 0 ? (
                        project?.documents.map((document, index) => (
                          <li key={index}>
                            <div className="d-flex align-items-center">
                              <span className="file-icon">
                                <i className="la la-file-alt" />
                              </span>
                              <p>{document.name}</p>
                            </div>
                            <div className="file-download">
                              <Link
                                onClick={() =>
                                  handleOpenInNewTab(document.file)
                                }
                              >
                                <i className="la la-download" />
                                Download
                              </Link>
                            </div>
                          </li>
                        ))
                      ) : (
                        <li>No documents available</li>
                      )}
                    </ul>
                  </div>
                </div>
              </div>
              <div className="col-xl-9">
                <div className="contact-tab-view">
                  <div className="tab-content pt-0">
                    <div className="tab-pane active show" id="activities">
                      <div className="contact-activity">
                        <ul>
                          <li className="activity-wrap">
                            <span className="activity-icon bg-warning">
                              <i className="las la-file-alt" />
                            </span>
                            <div className="activity-info">
                              <h4>Description</h4>
                              <p>{project?.description || ""}</p>
                            </div>
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProjectDetails;
