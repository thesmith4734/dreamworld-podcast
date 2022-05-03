import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useParams } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
    card: {
        marginBottom: theme.spacing(7),
        marginTop: theme.spacing(7),
        width: '90%',
        height: '50px',
        borderRadius: '5px',
        backgroundColor: '#FBDD96',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    }
}));

export default function PodcastPage(props) {
    const classes = useStyles();
    const [podcastData, setPodcastData] = useState([]);
    const { id } = useParams()

    useEffect(() => {
        const apiUrl = `/api/podcast/${id}`
        const requestParams = {
            method: "GET"
        }
        const fetchPodcasts = async () => {
            try {
                const response = await fetch(apiUrl, requestParams);
                const json = await response.json();
                console.log(json);
                setPodcastData(json)
            } catch (error) {
                console.log("error", error);
            }
        };
    
        fetchPodcasts();
    }, []);

    return(
        <div className={classes.background}>
            <div>
                <h2>{ podcastData.title }</h2>
                <h2>{ podcastData.description }</h2>
            </div>
        </div>
    )
}