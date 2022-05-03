import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom'

const useStyles = makeStyles((theme) => ({
    infobg: {
        width: '90%',
        height: '200px',
        margin: 'auto',
        position: 'relative',
        marginBottom: theme.spacing(7),
        marginTop: theme.spacing(7),
    },
    card: {
        width: '100%',
        height: '50%',
        borderRadius: '15px',
        backgroundColor: theme.palette.textbg.main,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        margin:'auto',
        position: 'absolute',
        bottom: '3px',
        border: '3px solid #000000',
    },
    image: {
        width: '200px',
        height: '200px',
        backgroundColor: theme.palette.primary.main,
        borderRadius: '15px',
        position: 'absolute',
        top: '0',
        border: '3px solid #000000',
    }
}));

export default function PodcastTitle(props) {
    const classes = useStyles();

    return(
        <div className={ classes.infobg }>
            <div className={ classes.card }>
                <Link to={`podcasts/${props.url}`}>
                    <span>{props.title}</span>
                </Link>
            </div>
            <div className={ classes.image }>
                <h2>Podcast Image</h2>
            </div>
        </div>
    )
}