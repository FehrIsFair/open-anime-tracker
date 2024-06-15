import React from "react";
import { Box, Typography } from "@mui/material";

import { h1 } from "../TextFormating/text_config";
import InputComponent from "../FormComps/InputComp";
import { AnimeTypeEnum, StatusEnum, ContentRating } from "../Enums/AnimeType";
import SelectComponent from "../FormComps/SelectComp";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import Anime from "../Models/anime";
import { animePost } from "../BackendRequests/anime";
import NumberInputComponent from "../FormComps/NumberInput";
import TextAreaComponent from "../FormComps/TextAreaComp";
import CheckBoxComponent from "../FormComps/CheckBoxComp";

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

  const submitForm = () => {
    const request_json: Anime = {
      rating: null,
      title: animeTitle,
      jp_title: jpTitle,
      _type: animeType,
      seasons: seasons,
      episodes: episodes,
      desc: desc,
      status: status,
      content_rating: contentRating,
      nsfw: nsfw,
    };
    animePost(request_json);
  };

  return (
    <Box>
      <Typography variant="h1" sx={h1}>
        Create an anime
      </Typography>
      <InputComponent
        id="anime-title"
        label="Title"
        value={animeTitle}
        set_field={setAnimeTitle}
      />
      <InputComponent
        id="jp-title"
        label="JP Title"
        value={jpTitle}
        set_field={setJpTitle}
      />
      <NumberInputComponent
        id="number-seasons"
        label="# of Seasons"
        value={seasons}
        set_field={setSeasons}
      />
      <NumberInputComponent
        id="number-episodes"
        label="# of Episodes"
        value={episodes}
        set_field={setEpisodes}
      />
      <TextAreaComponent
        id="description"
        value={desc}
        set_field={setDesc}
        placeholder="A boy named Satou Satou is looking to become the best plastic sergeon..."
      />
      <SelectComponent
        id="AnimeTypeSelect"
        label_id="anime-type"
        value={animeType}
        setValue={setAnimeType}
        menu_options={AnimeTypeEnum}
      />
      <SelectComponent
        id="StatusSelect"
        label_id="status"
        value={status}
        setValue={setStatus}
        menu_options={StatusEnum}
      />
      <SelectComponent
        id="ContentSelect"
        label_id="content-rating"
        value={contentRating}
        setValue={setContentRating}
        menu_options={ContentRating}
      />
      <CheckBoxComponent value={nsfw} set_value={setNsfw} label="NSFW" />
      <SubmitBtn variant={2} submit_func={submitForm}></SubmitBtn>
    </Box>
  );
};
export default AddAnime;
