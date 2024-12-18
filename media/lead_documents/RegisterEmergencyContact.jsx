import React, { useContext } from "react";
import { useForm, Controller } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import UserContext from "../../../contexts/UserContext";
import { registerUserData } from "../../../helpers/users";
import { Button } from "@mui/material";

const schema = yup.object({
  emergency_contact_primary_name: yup.string()
  .required("Name is required")
  .matches(/^[A-Za-z\s]+$/, "Name must contain only letters"),
  emergency_contact_primary_phone: yup
    .string()
    .required("Contact Number is required")
    .matches(/^\d+$/, "Number must contain only digits")
    .trim(),
    emergency_contact_primary_relationship: yup
    .string()
    .required("Relationship required")
    .trim(),
    emergency_contact_secondary_name: yup.string()
    .required("Name is required")
    .matches(/^[A-Za-z\s]+$/, "Name must contain only letters"),
    emergency_contact_secondary_phone: yup
    .string()
    .required("Contact Number is required")
    .matches(/^\d+$/, "Number must contain only digits")
    .trim(),
  emergency_contact_secondary_relationship: yup
    .string()
    .required("Relationship required")
    .trim(),
});

const RegisterEmergencyContact = (props) => {
  const { setActiveStep, formData, setFormData, setprofileID, profileID } = useContext(UserContext);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: formData,
  });
  const onSubmit = async (data) => {
    console.log("EmergencyContact", data);
    setFormData(data);
    try {
      const result = await registerUserData(formData);
      if (result === true) {
        console.log("result ",result)
        setprofileID(localStorage.getItem("ProfileId"))
        console.log("setprofileID", profileID);
        setActiveStep(4);
      } else {
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [name]: value,
    }));
  };
  const handleBack = () => {
    setActiveStep(2);
  };
  return (
    <div className="container">
      <div className="account-box">
        <div className="account-wrapper">
          <h3 className="account-title">Emergency Contact</h3>
          <div>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="input-block mb-3">
                <label>Name</label>
                <Controller
                  name="emergency_contact_primary_name"
                  control={control}
                  render={({ field }) => (
                    <input
                      className={`form-control ${
                        errors?.emergency_contact_primary_name
                          ? "error-input"
                          : ""
                      }`}
                      type="text"
                      onChange={(e) => {
                        field.onChange(e);
                        handleInputChange(e);
                      }}
                      {...field}
                    />
                  )}
                />
                <span className="text-danger">
                  {errors?.emergency_contact_primary_name?.message}
                </span>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label>Contact Number</label>
                  <Controller
                    name="emergency_contact_primary_phone"
                    control={control}
                    render={({ field }) => (
                      <input
                        className={`form-control ${
                          errors?.emergency_contact_primary_phone
                            ? "error-input"
                            : ""
                        }`}
                        type="text"
                        onChange={(e) => {
                          field.onChange(e);
                          handleInputChange(e);
                        }}
                        {...field}
                      />
                    )}
                  />
                  <span className="text-danger">
                    {errors?.emergency_contact_primary_phone?.message}
                  </span>
                </div>
                <div className="col-md-6 mb-3">
                  <label>Relation</label>
                  <Controller
                    name="emergency_contact_primary_relationship"
                    control={control}
                    render={({ field }) => (
                      <input
                        className={`form-control ${
                          errors?.emergency_contact_primary_relationship
                            ? "error-input"
                            : ""
                        }`}
                        type="text"
                        onChange={(e) => {
                          field.onChange(e);
                          handleInputChange(e);
                        }}
                        {...field}
                      />
                    )}
                  />
                  <span className="text-danger">
                    {errors?.emergency_contact_primary_relationship?.message}
                  </span>
                </div>
              </div>
              <div className="input-block mb-3">
                <label>Name</label>
                <Controller
                  name="emergency_contact_secondary_name"
                  control={control}
                  render={({ field }) => (
                    <input
                      className={`form-control ${
                        errors?.emergency_contact_secondary_name
                          ? "error-input"
                          : ""
                      }`}
                      type="text"
                      onChange={(e) => {
                        field.onChange(e);
                        handleInputChange(e);
                      }}
                      {...field}
                    />
                  )}
                />
                <span className="text-danger">
                  {errors?.emergency_contact_secondary_name?.message}
                </span>
              </div>
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label>Contact Number</label>
                  <Controller
                    name="emergency_contact_secondary_phone"
                    control={control}
                    render={({ field }) => (
                      <input
                        className={`form-control ${
                          errors?.emergency_contact_secondary_phone
                            ? "error-input"
                            : ""
                        }`}
                        type="text"
                        onChange={(e) => {
                          field.onChange(e);
                          handleInputChange(e);
                        }}
                        {...field}
                      />
                    )}
                  />
                  <span className="text-danger">
                    {errors?.emergency_contact_secondary_phone?.message}
                  </span>
                </div>
                <div className="col-md-6 mb-3">
                  <label>Relation</label>
                  <Controller
                    name="emergency_contact_secondary_relationship"
                    control={control}
                    render={({ field }) => (
                      <input
                        className={`form-control ${
                          errors?.emergency_contact_secondary_relationship
                            ? "error-input"
                            : ""
                        }`}
                        type="text"
                        onChange={(e) => {
                          field.onChange(e);
                          handleInputChange(e);
                        }}
                        {...field}
                      />
                    )}
                  />
                  <span className="text-danger">
                    {errors?.emergency_contact_secondary_relationship?.message}
                  </span>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div
        style={{
          position: "fixed",
          display: "flex",
          justifyContent: "space-between",
          bottom: "20px",
          width: "500px",
        }}
      >
        <Button
          disabled={false}
          onClick={handleBack}
          variant="outlined"
          style={{ width: "150px", marginLeft: "5px" }}
        >
          Back
        </Button>
        <Button
          type="submit"
          disabled={false}
          onClick={handleSubmit(onSubmit)}
          variant="contained"
          color="primary"
          style={{ width: "150px", marginRight: "5px" }}
        >
          Next
        </Button>
      </div>
    </div>
  );
};

export default RegisterEmergencyContact;
