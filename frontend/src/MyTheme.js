import { createTheme, responsiveFontSizes } from '@material-ui/core/styles';

let theme = createTheme({
    palette: {
        primary: {
            main: '#4F4F4F'
        },
        secondary: {
            main: '#C297B8'
        },
        textbg: {
            main: '#FBDD96'
        },
        divider: '#385F71',
        text: {
            primary: '#F5F0F6',
            secondary: '#F5F0F6'
        }
    },
});

theme = responsiveFontSizes(theme);

export default theme;