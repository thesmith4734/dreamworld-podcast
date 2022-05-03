import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import PodcastTitle from './podcast-title';

const useStyles = makeStyles((theme) => ({
    listbg: {
        marginBottom: theme.spacing(7),
        marginTop: theme.spacing(7),
        paddingTop: theme.spacing(4),
        paddingBottom: theme.spacing(4),
        width: '50%',
        backgroundColor: theme.palette.secondary.main,
        borderRadius: '10px',
        margin: 'auto',
    }
}));

export default function PodcastList() {
    const classes = useStyles();
    const [podcastList, setPodcastList] = useState([]);

    useEffect(() => {
        const apiUrl = '/api/podcasts'
        const fetchPodcasts = async () => {
            try {
                const response = await fetch(apiUrl, 
                    {
                        method: "GET"
                    });
                const json = await response.json();
                console.log(json);
                setPodcastList(json)
            } catch (error) {
                console.log("error", error);
            }
        };
    
        fetchPodcasts();
    }, []);

    
    return (
        <div className= {classes.listbg}>
            {podcastList.map((data, key) => (
                <PodcastTitle key={key} title={data.title} url={data.s3_foldername}/>
            ))}
        </div>
    )
}
