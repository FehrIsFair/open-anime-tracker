import React, { useContext } from "react";
import { Box, Typography } from "@mui/material";
import { Navigate } from "react-router-dom";

import { h1 } from "../TextFormating/text_config";
import InputComponent from "../FormComps/InputComp";
import { AnimeTypeEnum, StatusEnum, ContentRating } from "../Enums/AnimeType";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import NumberInputComponent from "../FormComps/NumberInput";
import TextAreaComponent from "../FormComps/TextAreaComp";
import CheckBoxComponent from "../FormComps/CheckBoxComp";
import SelectComponent from "../FormComps/SelectComp";
import { animePost } from "../BackendRequests/anime";
import { AuthContext } from "../context/auth_context";

const AddAnime = () => {
  const [animeType, setAnimeType] = React.useState("show");
  const [status, setStatus] = React.useState("pending");
  const [contentRating, setContentRating] = React.useState("PG");
  const [animeTitle, setAnimeTitle] = React.useState("");
  const [desc, setDesc] = React.useState("");
  const [jpTitle, setJpTitle] = React.useState("");
  const [seasons, setSeasons] = React.useState(1);
  const [episodes, setEpisodes] = React.useState(1);
  const [nsfw, setNsfw] = React.useState(false);
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const { user } = useContext(AuthContext);

  const submitForm = async () => {
    setError("");

    if (!animeTitle.trim()) {
      setError("Title is required.");
      return;
    }

    setLoading(true);
    try {
      const request = {
        rating: null,
        title: animeTitle.trim(),
        jp_title: jpTitle.trim(),
        _type: animeType,
        seasons,
        episodes,
        desc,
        status,
        content_rating: contentRating,
        nsfw,
      };
      await animePost(request);
      // Optionally reset form or redirect after success
    } catch (err: any) {
      setError(err.response?.data?.message || "Failed to create anime entry.");
    } finally {
      setLoading(false);
    }
  };

  if (user == null) {
    return <Navigate to="/signin" />;
  }

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h1" sx={h1}>
        Create an Anime
      </Typography>
      <InputComponent
        id="anime-title"
        label="Title"
        value={animeTitle}
        onChange={setAnimeTitle}
        testId="qa-anime_title-input"
      />
      <InputComponent
        id="jp-title"
        label="JP Title"
        value={jpTitle}
        onChange={setJpTitle}
        testId="qa-anime_jp_title-input"
      />
      <NumberInputComponent
        id="number-seasons"
        label="# of Seasons"
        value={seasons}
        onChange={setSeasons}
        testId="qa-anime_seasons-input"
      />
      <NumberInputComponent
        id="number-episodes"
        label="# of Episodes"
        value={episodes}
        onChange={setEpisodes}
        testId="qa-anime_episodes-input"
      />
      <TextAreaComponent
        id="description"
        label="Description"
        value={desc}
        onChange={setDesc}
        placeholder="A boy named Satou Satou is looking to become the best plastic surgeon..."
        testId="qa-anime_desc-input"
      />
      <SelectComponent
        id="AnimeTypeSelect"
        label="Type"
        value={animeType}
        onChange={setAnimeType}
        options={AnimeTypeEnum}
        testId="qa-anime_type-select"
      />
      <SelectComponent
        id="StatusSelect"
        label="Status"
        value={status}
        onChange={setStatus}
        options={StatusEnum}
        testId="qa-anime_status-select"
      />
      <SelectComponent
        id="ContentSelect"
        label="Content Rating"
        value={contentRating}
        onChange={setContentRating}
        options={ContentRating}
        testId="qa-anime_content_rating-select"
      />
      <CheckBoxComponent
        value={nsfw}
        onChange={setNsfw}
        label="NSFW"
        testId="qa-anime_nsfw-toggle"
      />
      {error && <Typography color="error" sx={{ mt: 1, fontSize: "0.875rem" }} data-testid="qa-add_anime_error-error">{error}</Typography>}
      <SubmitBtn
        variant="contained"
        onSubmit={submitForm}
        disabled={loading}
        sx={{ mt: 2 }}
        testId="qa-add_anime_submit-submit"
      >
        {loading ? "Saving..." : "Submit"}
      </SubmitBtn>
    </Box>
  );
};
export default AddAnime;
