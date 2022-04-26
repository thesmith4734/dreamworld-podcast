import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import PodcastTitle from './podcast-title';

const useStyles = makeStyles((theme) => ({
    card: {
        marginBottom: theme.spacing(7),
        marginTop: theme.spacing(7),
        width: '90%',
        height: '100px',
        backgroundColor: theme.palette.secondary.main,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    }
}));

export default function TestComponent() {
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
        <div>
            {podcastList.map((data, key) => (
                <PodcastTitle key={key} title={data.title} url={data.s3_foldername}/>
            ))}
        </div>
    )
}
